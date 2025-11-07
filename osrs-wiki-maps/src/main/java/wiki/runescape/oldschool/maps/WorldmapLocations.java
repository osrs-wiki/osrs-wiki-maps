package wiki.runescape.oldschool.maps;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import net.runelite.cache.io.InputStream;
import net.runelite.cache.region.Location;
import net.runelite.cache.region.Position;

@Slf4j
public class WorldmapLocations
{
	private static final int HAS_OVERLAY = 2;
	private static final int HAS_LOCATION = 4;

	public static List<Location> load(InputStream b)
	{
		ArrayList<Location> locs = new ArrayList<>();
		for (int localX = 0; localX < 64; ++localX)
		{
			for (int localY = 0; localY < 64; ++localY)
			{
				locs.addAll(unpackColumn(localX, localY, b));
			}
		}
		return locs;
	}

	private static List<Location> unpackColumn(int x, int y, InputStream buffer)
	{
		int settings = buffer.readUnsignedByte();
		if (settings != 0) {
			if ((settings & 1) != 0) {
				unpackColumnSimple(x, y, buffer, settings);
			} else {
				return unpackColumnComplex(x, y, buffer, settings);
			}
		}
		return Collections.emptyList();
	}

	private static void unpackColumnSimple(int x, int y, InputStream buffer, int settings)
	{
		boolean hasOverlay = (settings & HAS_OVERLAY) != 0;
		if (hasOverlay) {
			buffer.readUnsignedShort();
			// overlays[0][x][y] = (short) buffer.readUnsignedShort();
		}
		buffer.readUnsignedShort();
		// underlays[0][x][y] = (short) buffer.readUnsignedShort();
	}

	private static List<Location> unpackColumnComplex(int x, int y, InputStream buffer, int settings)
	{
		int levelCount = ((settings & 24) >> 3) + 1;
		boolean hasOverlay = (settings & HAS_OVERLAY) != 0;
		boolean hasLocation = (settings & HAS_LOCATION) != 0;

		//Edges between water and land
		// unerlays[0][x][y] = buffer.readUnsignedShort();
		buffer.readUnsignedShort();
		if (hasOverlay)
		{
			int levels = buffer.readUnsignedByte();
			for (int level = 0; level < levels; ++level)
			{
				int overlay = buffer.readUnsignedShort();
				if (overlay != 0)
				{
					//Edges between water and land shape and rotation
					buffer.readUnsignedByte();
					// overlays[level][x][y] = (short) overlay;
					// int info = buffer.readUnsignedByte();
					// overlayShapes[level][x][y] = info >> 2;
					// overlayAngles[level][x][y] = info >> 3;
				}
			}
		}

		ArrayList<Location> locs = new ArrayList<>();
		if (hasLocation)
		{
			for (int level = 0; level < levelCount; ++level)
			{
				int count = buffer.readUnsignedByte();
				if (count != 0)
				{
					for (int i = 0; i < count; ++i)
					{
						int id = buffer.readBigSmart2();

						int info = buffer.readUnsignedByte();
						int type = info >> 2;
						int orientation = info & 0x3;

						Location loc = new Location(id, type, orientation, new Position(x, y, level));
						locs.add(loc);
					}
				}
			}
		}
		return locs;
	}
}