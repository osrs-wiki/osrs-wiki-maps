package wiki.runescape.oldschool.maps;


import net.runelite.cache.*;
import net.runelite.cache.definitions.WorldMapCompositeDefinition;
import net.runelite.cache.definitions.ZoneDefinition;
import net.runelite.cache.definitions.MapSquareDefinition;
import net.runelite.cache.definitions.loaders.WorldMapCompositeLoader;
import net.runelite.cache.fs.*;
import net.runelite.cache.region.Location;
import net.runelite.cache.region.Region;
import net.runelite.cache.region.RegionLoader;

import com.google.gson.Gson;
import net.runelite.cache.util.XteaKeyManager;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.*;
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

        Index index = store.getIndex(IndexType.WORLDMAP);
        Archive archive = index.getArchive(1);
        Storage storage = store.getStorage();
        byte[] archiveData = storage.loadArchive(archive);
        ArchiveFiles files = archive.getFiles(archiveData);

        WorldMapCompositeLoader loader = new WorldMapCompositeLoader();

        for (FSFile file : files.getFiles()) {
            WorldMapCompositeDefinition wmd = loader.load(file.getContents());
            int mapid = file.getFileId();

            List<MapSquareDefinition> mapSquareDefinitions = new ArrayList<>(wmd.getMapSquareDefinitions());
            List<ZoneDefinition> zoneDefinitions = new ArrayList<>(wmd.getZoneDefinitions());

            String msFilename = String.format("mapSquareDefinitions_%s.json", mapid);
            outputfile = fileWithDirectoryAssurance(dirname, msFilename);
            out = new PrintWriter(outputfile);
            json = gson.toJson(mapSquareDefinitions);
            out.write(json);
            out.close();

            String zFilename = String.format("zoneDefinitions_%s.json", mapid);
            outputfile = fileWithDirectoryAssurance(dirname, zFilename);
            out = new PrintWriter(outputfile);
            json = gson.toJson(zoneDefinitions);
            out.write(json);
            out.close();
        }
    }

    private static File fileWithDirectoryAssurance(String directory, String filename) {
        File dir = new File(directory);
        if (!dir.exists()) dir.mkdirs();
        return new File(directory + "/" + filename);
    }

    private static List<MinimapIcon> getMapIcons(Store store) throws Exception {
        List<MinimapIcon> icons = new ArrayList<MinimapIcon>();
        SpriteManager spriteManager = new SpriteManager(store);
        spriteManager.load();
        HashSet<Integer> spriteIds = new HashSet<Integer>();
        ObjectManager objectManager = new ObjectManager(store);
        objectManager.load();
        AreaManager areaManager = new AreaManager(store);
        areaManager.load();
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
            System.out.println(outputfile);
            ImageIO.write(iconImage, "png", outputfile);
        }
        return icons;
    }
}