package wiki.runescape.oldschool.maps;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashSet;
import lombok.extern.slf4j.Slf4j;
import net.runelite.cache.IndexType;
import net.runelite.cache.ObjectManager;
import net.runelite.cache.definitions.LocationsDefinition;
import net.runelite.cache.definitions.MapDefinition;
import net.runelite.cache.definitions.ObjectDefinition;
import net.runelite.cache.definitions.loaders.LocationsLoader;
import net.runelite.cache.definitions.loaders.MapLoader;
import net.runelite.cache.fs.Archive;
import net.runelite.cache.fs.Index;
import net.runelite.cache.fs.Storage;
import net.runelite.cache.fs.Store;
import net.runelite.cache.io.InputStream;
import net.runelite.cache.region.Location;
import net.runelite.cache.util.KeyProvider;

@Slf4j
public class RegionLoader extends net.runelite.cache.region.RegionLoader
{
	private static final int MAX_REGION = 32768;

	private static final int _MIN_REGION_OVERWORLD = 3872;
	private static final int _MAX_REGION_OVERWORLD = 15937;
	private static final int MIN_REGION_OVERWORLD_X = _MIN_REGION_OVERWORLD >> 8;
	private static final int MAX_REGION_OVERWORLD_X = _MAX_REGION_OVERWORLD >> 8;
	private static final int MIN_REGION_OVERWORLD_Y = _MIN_REGION_OVERWORLD & 0xFF;
	private static final int MAX_REGION_OVERWORLD_Y = _MAX_REGION_OVERWORLD & 0xFF;

	private final Store store;
	private final Index indexWorldmap;
	private final Index indexMinimap;
	private final KeyProvider keyProvider;
	private final ObjectManager objectManager;

	public RegionLoader(Store store, KeyProvider keyProvider, ObjectManager objectManager)
	{
		super(store, keyProvider);

		this.store = store;
		indexMinimap = store.getIndex(IndexType.MAPS);
		indexWorldmap = store.getIndex(IndexType.WORLDMAP_GEOGRAPHY);
		this.keyProvider = keyProvider;
		this.objectManager = objectManager;
	}

	@Override
	public void loadRegions() throws IOException
	{
		if (!super.getRegions().isEmpty())
		{
			return;
		}

		Storage storage = store.getStorage();

		// Load overworld locations
		// TODO: ideally want to findArchiveByName rather than looping over all, but names are hashed and unknown
		// TODO: do this for everything, not just overworld
		HashSet<Integer> seenRegions = new HashSet<>();
		for (Archive a : indexWorldmap.getArchives())
		{
			byte[] data = a.decompress(storage.loadArchive(a));
			InputStream buffer = new InputStream(data);

			int mapType = buffer.readUnsignedByte();
			int mapsquareX = buffer.readUnsignedByte();
			int mapsquareY = buffer.readUnsignedByte();
			int regionId = (mapsquareX << 8) + mapsquareY;

			boolean isOverworld =
				mapsquareX >= MIN_REGION_OVERWORLD_X &&
				mapsquareX <= MAX_REGION_OVERWORLD_X &&
				mapsquareY >= MIN_REGION_OVERWORLD_Y &&
				mapsquareY <= MAX_REGION_OVERWORLD_Y;

			if (mapType == 0 && isOverworld)
			{
				MapDefinition mapDef = loadMapDefinition(regionId, storage);
				LocationsDefinition locDef = loadLocationDefinitionOverworld(regionId, storage, buffer);
				if (locDef != null && mapDef != null)
				{
					loadRegion(regionId, mapDef, locDef);
					seenRegions.add(regionId);
				}
			}
		}

		log.info("Loaded {} overworld regions", seenRegions.size());

		// Load non-overworld locations
		for (int regionId = 0; regionId < MAX_REGION; ++regionId)
		{
			if (seenRegions.contains(regionId))
			{
				continue;
			}
			try
			{
				MapDefinition mapDef = loadMapDefinition(regionId, storage);
				LocationsDefinition locDef = loadLocationDefinitionSimple(regionId, storage);
				if (mapDef != null && locDef != null)
				{
					loadRegion(regionId, mapDef, locDef);
					seenRegions.add(regionId);
				}
			}
			catch (IOException ex)
			{
				log.debug("Can't decrypt region " + regionId, ex);
			}
		}

		log.info("Loaded {} total regions", seenRegions.size());
	}

	public MapDefinition loadMapDefinition(int regionId, Storage storage) throws IOException
	{
		int x = regionId >> 8;
		int y = regionId & 0xFF;

		Archive mapArchive = indexMinimap.findArchiveByName("m" + x + "_" + y);

		if (mapArchive == null)
		{
			return null;
		}

		byte[] mapData = mapArchive.decompress(storage.loadArchive(mapArchive));
		return new MapLoader().load(x, y, mapData);
	}

	public LocationsDefinition loadLocationDefinitionOverworld(int regionId, Storage storage, InputStream worldmapBuffer) throws IOException
	{
		int x = regionId >> 8;
		int y = regionId & 0xFF;

		ArrayList<Location> locations = new ArrayList<>();

		LocationsDefinition locDef = loadLocationDefinitionSimple(regionId, storage);
		if (locDef != null)
		{
			for (Location l : locDef.getLocations())
			{
				int id = l.getId();
				ObjectDefinition od = objectManager.getObject(id);
				boolean isMapIcon = od.getMapAreaId() != -1;
				boolean isUpstairs = l.getPosition().getZ() > 0;

				if (!isMapIcon && isUpstairs)
				{
					locations.add(l);
				}
			}
		}

		locations.addAll(WorldmapLocations.load(worldmapBuffer));

		locDef = new LocationsDefinition();
		locDef.setRegionX(x);
		locDef.setRegionY(y);
		locDef.setLocations(locations);
		return locDef;
	}

	public LocationsDefinition loadLocationDefinitionSimple(int regionId, Storage storage) throws IOException
	{
		int x = regionId >> 8;
		int y = regionId & 0xFF;

		Archive locArchive = indexMinimap.findArchiveByName("l" + x + "_" + y);

		if (locArchive == null)
		{
			return null;
		}

		int[] keys = keyProvider.getKey(regionId);
		if (keys != null)
		{
			byte[] locDataMinimap = locArchive.decompress(storage.loadArchive(locArchive), keys);
			return new LocationsLoader().load(x, y, locDataMinimap);
		}

		return null;
	}
}