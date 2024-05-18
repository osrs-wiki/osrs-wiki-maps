package wiki.runescape.oldschool.maps;


import net.runelite.cache.AreaManager;
import net.runelite.cache.IndexType;
import net.runelite.cache.MapImageDumper;
import net.runelite.cache.ObjectManager;
import net.runelite.cache.SpriteManager;
import net.runelite.cache.definitions.AreaDefinition;
import net.runelite.cache.definitions.ObjectDefinition;
import net.runelite.cache.definitions.SpriteDefinition;
import net.runelite.cache.definitions.WorldMapDefinition;
import net.runelite.cache.definitions.loaders.WorldMapLoader;
import net.runelite.cache.fs.Archive;
import net.runelite.cache.fs.ArchiveFiles;
import net.runelite.cache.fs.FSFile;
import net.runelite.cache.fs.Index;
import net.runelite.cache.fs.Storage;
import net.runelite.cache.fs.Store;
import net.runelite.cache.region.Location;
import net.runelite.cache.region.Region;
import net.runelite.cache.region.RegionLoader;

import com.google.gson.Gson;
import net.runelite.cache.util.XteaKeyManager;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileInputStream;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;

public class MapExport {
    private static RegionLoader regionLoader;
    private static String version = "2024-05-15_c";
    public static void main(String[] args) throws Exception {
        version = args.length > 0 ? args[0] : version;
        Gson gson = new Gson();
        String cache = "./data/cache";
        Store store = new Store(new File(cache));
        store.load();

        XteaKeyManager xteaKeyManager = new XteaKeyManager();
        try (FileInputStream fin = new FileInputStream("./data/xteas.json"))
        {
            xteaKeyManager.loadKeys(fin);
        }

        regionLoader = new RegionLoader(store, xteaKeyManager);

        MapImageDumper dumper = new MapImageDumper(store, xteaKeyManager);
        dumper.setRenderIcons(false);
        dumper.setLowMemory(false);
        dumper.setRenderLabels(false);
        dumper.load();

        for (int plane = 0; plane < 4; plane++) {
            BufferedImage image = dumper.drawMap(plane);
            String dirname = String.format("./out/mapgen/versions/%s/tiles/base", version);
            String filename = String.format("plane_%s.png", plane);
            File outputfile = fileWithDirectoryAssurance(dirname, filename);
            System.out.println(outputfile);
            ImageIO.write(image, "png", outputfile);
        }

        String dirname = String.format("./out/mapgen/versions/%s", version);
        String filename = "minimapIcons.json";
        File outputfile = fileWithDirectoryAssurance(dirname, filename);
        PrintWriter out = new PrintWriter(outputfile);
        List<MinimapIcon> icons = getMapIcons(store);
        String json = gson.toJson(icons);
        out.write(json);
        out.close();

        filename = "worldMapDefinitions.json";
        outputfile = fileWithDirectoryAssurance(dirname, filename);
        out = new PrintWriter(outputfile);
        List<WorldMapDefinition> wmds = getWorldMapDefinitions(store);
        json = gson.toJson(wmds);
        out.write(json);
        out.close();
    }

    private static File fileWithDirectoryAssurance(String directory, String filename) {
        File dir = new File(directory);
        if (!dir.exists()) dir.mkdirs();
        return new File(directory + "/" + filename);
    }

    private static List<WorldMapDefinition> getWorldMapDefinitions(Store store) throws Exception {
        Index index = store.getIndex(IndexType.WORLDMAP);
        Archive archive = index.findArchiveByName("details");
        Storage storage = store.getStorage();
        byte[] archiveData = storage.loadArchive(archive);
        ArchiveFiles files = archive.getFiles(archiveData);

        WorldMapLoader loader = new WorldMapLoader();

        List<WorldMapDefinition> definitions = new ArrayList<>();
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
        regionLoader.loadRegions();
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

        for (int spriteId : spriteIds) {
            SpriteDefinition sprite = spriteManager.findSprite(spriteId, 0);
            BufferedImage iconImage = spriteManager.getSpriteImage(sprite);
            String dirname = String.format("./out/mapgen/versions/%s/icons", version);
            String filename = String.format("%s.png", spriteId);
            File outputfile = fileWithDirectoryAssurance(dirname, filename);
            ImageIO.write(iconImage, "png", outputfile);
        }
        return icons;
    }
}