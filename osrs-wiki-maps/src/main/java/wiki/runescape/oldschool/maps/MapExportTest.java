package wiki.runescape.oldschool.maps;

import com.google.gson.Gson;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileInputStream;
import java.util.Scanner;
import javax.imageio.ImageIO;
import lombok.extern.slf4j.Slf4j;
import net.runelite.cache.MapImageDumper;
import net.runelite.cache.ObjectManager;
import net.runelite.cache.fs.Store;
import net.runelite.cache.util.XteaKeyManager;

@Slf4j
public class MapExportTest
{
	public static void main(String[] args) throws Exception
	{
		String versionPath = "./data/versions/version.txt";
		File versionTxt = new File(versionPath);
		Scanner sc = new Scanner(versionTxt);
		String version = sc.next();
		log.info("Version: " + version);

		String intermediateDir = String.format("./out/mapgen/versions/%s", version);
		String outputDir = String.format("%s/output", intermediateDir);
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

		ObjectManager objectManager = new ObjectManager(store);
		objectManager.load();

		RegionLoader regionLoader = new RegionLoader(store, xteaKeyManager, objectManager);
		regionLoader.loadRegions();

		MapImageDumper dumper = new MapImageDumper(store, regionLoader);
		dumper.setRenderIcons(true);
		dumper.setRenderLabels(true);
		dumper.setLowMemory(false);
		dumper.load();

		for (int plane = 0; plane < 4; plane++)
		{
			BufferedImage im = dumper.drawMap(plane);
			String filename = String.format("test_%s.png", plane);
			File outputfile = fileWithDirectoryAssurance(outputDir, filename);
			ImageIO.write(im, "png", outputfile);
		}
	}

	private static File fileWithDirectoryAssurance(String directory, String filename) {
		File dir = new File(directory);
		if (!dir.exists()) dir.mkdirs();
		return new File(directory + "/" + filename);
	}
}