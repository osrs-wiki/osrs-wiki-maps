package wiki.runescape.oldschool.maps;

import com.google.gson.Gson;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileInputStream;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Scanner;
import javax.imageio.ImageIO;
import lombok.extern.slf4j.Slf4j;
import net.runelite.cache.AreaManager;
import net.runelite.cache.IndexType;
import net.runelite.cache.MapImageDumper;
import net.runelite.cache.ObjectManager;
import net.runelite.cache.SpriteManager;
import net.runelite.cache.WorldMapManager;
import net.runelite.cache.definitions.AreaDefinition;
import net.runelite.cache.definitions.ObjectDefinition;
import net.runelite.cache.definitions.SpriteDefinition;
import net.runelite.cache.definitions.WorldMapDefinition;
import net.runelite.cache.definitions.WorldMapElementDefinition;
import net.runelite.cache.definitions.loaders.WorldMapLoader;
import net.runelite.cache.fs.Archive;
import net.runelite.cache.fs.ArchiveFiles;
import net.runelite.cache.fs.FSFile;
import net.runelite.cache.fs.Index;
import net.runelite.cache.fs.Storage;
import net.runelite.cache.fs.Store;
import net.runelite.cache.region.Location;
import net.runelite.cache.region.Region;
import net.runelite.cache.util.XteaKeyManager;

@Slf4j
public class MapExport {
    private static RegionLoader regionLoader;
	private static ObjectManager objectManager;
	private static String  outputDir;

    public static void main(String[] args) throws Exception {
        String versionPath = "./data/versions/version.txt";
        File versionTxt = new File(versionPath);
        Scanner sc = new Scanner(versionTxt);
		String version = sc.next();
        log.info("Version: " + version);

        String intermediateDir = String.format("./out/mapgen/versions/%s", version);
        outputDir = String.format("%s/output", intermediateDir);
        String cacheDir = String.format("./data/versions/%s", version);

        Gson gson = new Gson();
        String cache = String.format("%s/cache", cacheDir);
        Store store = new Store(new File(cache));
        store.load();
        log.info("Cache loaded: " + cache);

        String xteas = String.format("%s/xteas.json", cacheDir);
        XteaKeyManager xteaKeyManager = new XteaKeyManager();
        try (FileInputStream fin = new FileInputStream(xteas))
        {
            xteaKeyManager.loadKeys(fin);
        }

		objectManager = new ObjectManager(store);
		objectManager.load();

		regionLoader = new RegionLoader(store, xteaKeyManager, objectManager);
		regionLoader.loadRegions();

		MapImageDumper dumper = new MapImageDumper(store, regionLoader);
		dumper.setRenderIcons(false);
		dumper.setRenderLabels(false);
		dumper.setLowMemory(false);
		dumper.load();

        for (Region region : regionLoader.getRegions()) {
            int x = region.getRegionX();
            int y = region.getRegionY();
            String dirname = String.format("%s/tiles/base", intermediateDir);
            for (int plane = 0; plane < 4; plane++) {
                BufferedImage reg = dumper.drawRegion(region, plane);
                String filename = String.format("%s_%s_%s.png", plane, x, y);
                File outputfile = fileWithDirectoryAssurance(dirname, filename);
                ImageIO.write(reg, "png", outputfile);
            }
        }
        log.info("Maps generated for " + regionLoader.getRegions().size() + " regions");

        String filename = "minimapIcons.json";
        File outputfile = fileWithDirectoryAssurance(intermediateDir, filename);
        PrintWriter out = new PrintWriter(outputfile);
        List<MinimapIcon> icons = getMapIcons(store);
        String json = gson.toJson(icons);
        out.write(json);
        out.close();
        log.info("Minimap icon definitions generated");

        filename = "worldMapDefinitions.json";
        outputfile = fileWithDirectoryAssurance(intermediateDir, filename);
        out = new PrintWriter(outputfile);
        List<WorldMapDefinition> definitions = getWorldMapDefinitions(store);
        json = gson.toJson(definitions);
        out.write(json);
        out.close();
        log.info("World map definitions generated");
    }

    private static File fileWithDirectoryAssurance(String directory, String filename) {
        File dir = new File(directory);
        if (!dir.exists()) dir.mkdirs();
        return new File(directory + "/" + filename);
    }

    private static List<WorldMapDefinition> getWorldMapDefinitions(Store store) throws Exception {
        List<WorldMapDefinition> definitions = new ArrayList<>();
        WorldMapLoader loader = new WorldMapLoader();
        Index index = store.getIndex(IndexType.WORLDMAP);

        Archive archive = index.findArchiveByName("details");

        Storage storage = store.getStorage();
        byte[] archiveData = storage.loadArchive(archive);
        ArchiveFiles files = archive.getFiles(archiveData);

        for (FSFile file : files.getFiles()) {
            WorldMapDefinition wmd = loader.load(file.getContents(), file.getFileId());
            definitions.add(wmd);
        }
        return definitions;
    }

    private static List<MinimapIcon> getMapIcons(Store store) throws Exception {
        List<MinimapIcon> icons = new ArrayList<>();
        SpriteManager spriteManager = new SpriteManager(store);
        spriteManager.load();
        HashSet<Integer> spriteIds = new HashSet<>();
        AreaManager areaManager = new AreaManager(store);
        areaManager.load();
        WorldMapManager worldMapManager = new WorldMapManager(store);
        worldMapManager.load();
        List<WorldMapElementDefinition> elements = worldMapManager.getElements();

        for (Region region : regionLoader.getRegions()) {
            for (Location location : region.getLocations()) {
                ObjectDefinition od = objectManager.getObject(location.getId());

                if (od.getMapAreaId() != -1) {
                    AreaDefinition area = areaManager.getArea(od.getMapAreaId());
                    icons.add(new MinimapIcon(location.getPosition(), area.spriteId));
                    spriteIds.add(area.spriteId);
                }
            }
        }

        for (WorldMapElementDefinition element : elements) {
            AreaDefinition area = areaManager.getArea(element.getAreaDefinitionId());
            if (area.spriteId == -1) {  // maybe these are the yellow squares/lines, no sprite?
                continue;
            }
            icons.add(new MinimapIcon(element.getWorldPosition(), area.spriteId));
            spriteIds.add(area.spriteId);
        }

        for (int spriteId : spriteIds) {
            SpriteDefinition sprite = spriteManager.findSprite(spriteId, 0);
            BufferedImage iconImage = spriteManager.getSpriteImage(sprite);
            String dirname = String.format("%s/icons", outputDir);
            String filename = String.format("%s.png", spriteId);
            File outputfile = fileWithDirectoryAssurance(dirname, filename);
            ImageIO.write(iconImage, "png", outputfile);
        }
        return icons;
    }
}