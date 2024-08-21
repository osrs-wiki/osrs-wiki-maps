package wiki.runescape.oldschool.maps;

import net.runelite.cache.*;
import net.runelite.cache.definitions.AreaDefinition;
import net.runelite.cache.definitions.ObjectDefinition;
import net.runelite.cache.definitions.SpriteDefinition;
import net.runelite.cache.definitions.WorldMapDefinition;
import net.runelite.cache.definitions.WorldMapElementDefinition;
import net.runelite.cache.definitions.loaders.WorldMapLoader;
import net.runelite.cache.fs.*;
import net.runelite.cache.region.Location;
import net.runelite.cache.region.Region;
import net.runelite.cache.region.RegionLoader;

import com.google.gson.Gson;
import net.runelite.cache.util.XteaKeyManager;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.*;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Scanner;

public class MapExport {
    private static RegionLoader regionLoader;
    private static String version;
    private static String  outputDir;

    private static final Logger logger = LoggerFactory.getLogger(MapExport.class);
    public static void main(String[] args) throws Exception {
        String versionPath = "./data/versions/version.txt";
        File versionTxt = new File(versionPath);
        Scanner sc = new Scanner(versionTxt);
        version = sc.nextLine();
        logger.info("Version: " + version);

        List<Integer> regionDiffs = new ArrayList<>();
        while (sc.hasNextLine()) {
            String regionStr = sc.nextLine();
            if (regionStr.isEmpty()) {
                continue;
            }
            logger.info("Region: " + regionStr);
            int regionInt = Integer.parseInt(regionStr);
            regionDiffs.add(regionInt);
        }

        String intermediateDir = String.format("./out/mapgen/versions/%s", version);
        outputDir = String.format("%s/output", intermediateDir);
        String cacheDir = String.format("./data/versions/%s", version);

        Gson gson = new Gson();
        String cache = String.format("%s/cache", cacheDir);
        Store store = new Store(new File(cache));
        store.load();
        logger.info("Cache loaded: " + cache);

        String xteas = String.format("%s/xteas.json", cacheDir);
        XteaKeyManager xteaKeyManager = new XteaKeyManager();
        try (FileInputStream fin = new FileInputStream(xteas))
        {
            xteaKeyManager.loadKeys(fin);
        }

        MapImageDumper dumper = new MapImageDumper(store, xteaKeyManager);
        dumper.setRenderIcons(false);
        dumper.setRenderLabels(false);
        dumper.setLowMemory(false);
        dumper.load();
        regionLoader = new RegionLoader(store, xteaKeyManager);
        regionLoader.loadRegions();
        for (Region region : regionLoader.getRegions()) {
            int regionId = region.getRegionID();
            if (!regionDiffs.isEmpty() && !regionDiffs.contains(regionId)) {
                continue;
            }
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
        logger.info("Maps generated for " + regionLoader.getRegions().size() + " regions");

        String filename = "minimapIcons.json";
        File outputfile = fileWithDirectoryAssurance(intermediateDir, filename);
        PrintWriter out = new PrintWriter(outputfile);
        List<MinimapIcon> icons = getMapIcons(store);
        String json = gson.toJson(icons);
        out.write(json);
        out.close();
        logger.info("Minimap icon definitions generated");

        filename = "worldMapDefinitions.json";
        outputfile = fileWithDirectoryAssurance(intermediateDir, filename);
        out = new PrintWriter(outputfile);
        List<WorldMapDefinition> definitions = getWorldMapDefinitions(store);
        json = gson.toJson(definitions);
        out.write(json);
        out.close();
        logger.info("World map definitions generated");
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
        ObjectManager objectManager = new ObjectManager(store);
        objectManager.load();
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