# GitHub Copilot Instructions

## Project Overview

This is a multi-language toolkit for generating map images and data for the OSRS (Old School RuneScape) Wiki. The project combines Python scripts, Java applications, and configuration files to process OSRS cache data and generate comprehensive map imagery and metadata for wiki use.

## Architecture & Workflow

The project follows a 3-stage pipeline:

1. **Cache Download** (`cache.py`) - Downloads latest OSRS cache from archive.openrs2.org
2. **Map Generation** (`MapExport.java`) - Processes cache to generate base map tiles and definitions
3. **Map Assembly** (`stitch.py`) - Stitches tiles into final maps with icons and metadata

## Languages & Technologies

### Java (MapExport.java)
- **Version**: JDK 11 (specified in setup)
- **Build Tool**: Maven with `pom.xml`
- **Dependencies**: RuneLite cache library for OSRS cache processing
- **Purpose**: Extract map tiles, minimap icons, and world map definitions from OSRS cache

### Python (Scripts)
- **Version**: Python 3.x
- **Dependencies**: numpy, Pillow, python-dateutil, requests (see `requirements.txt`)
- **Purpose**: Cache management, image processing, and final map assembly

## Code Style & Guidelines

### Java Code Style
- **Indentation**: Use tabs (enforced by `checkstyle.xml`)
- **Braces**: New line style (left curly on new line, right curly alone)
- **Naming**: Follow Java conventions (PascalCase for classes, camelCase for methods/variables)
- **Structure**: Use RuneLite cache API patterns for data extraction

#### Java Code Example:
```java
public class MapExport {
    private static final Logger logger = LoggerFactory.getLogger(MapExport.class);
    
    public static void main(String[] args) throws Exception 
    {
        Store store = new Store(new File(cache));
        store.load();
        // Process cache data
    }
}
```

### Python Code Style
- **Style**: Follow PEP 8 conventions
- **Type Hints**: Use type hints where beneficial (seen in function signatures)
- **Imports**: Group standard library, third-party, and local imports
- **Functions**: Use descriptive names and docstrings for complex operations

#### Python Code Example:
```python
def load_defs(cache_defs: str, user_defs: str, base_tiles: str) -> dict:
    """
    Load worldMapDefinitions + user-defined defns + debug defn
    """
    with open(cache_defs) as f:
        defs = {int(d["fileId"]): d for d in json.load(f)}
    return defs
```

## File Organization & Data Flow

### Input/Output Structure
```
data/versions/{version_name}/
├── cache/                    # Raw OSRS cache files
└── xteas.json               # Encryption keys

out/mapgen/versions/{version_name}/
├── tiles/base/              # Raw map tiles (from Java)
├── minimapIcons.json        # Icon definitions (from Java)
├── worldMapDefinitions.json # Map definitions (from Java)
└── output/                  # Final processed output (from Python)
    ├── tiles/rendered/      # Final map images
    ├── icons/              # Processed map icons
    └── basemaps.json       # Wiki basemap definitions
```

### Key Components

#### Cache Processing (`cache.py`)
- Downloads latest cache from OpenRS2 archive
- Manages version naming and storage
- Handles XTEA key extraction for cache decryption

#### Map Export (`MapExport.java`)
- Uses RuneLite cache library to process OSRS cache data
- Generates base map tiles (4 planes per region)
- Extracts minimap icon definitions and world map definitions
- Outputs JSON metadata files

#### Map Assembly (`stitch.py`)
- Combines base tiles into complete maps
- Applies icons, labels, and visual enhancements
- Generates wiki-compatible basemap definitions
- Handles custom map definitions from `user_world_defs.json`

## Configuration Files

### User Map Definitions (`scripts/user_world_defs.json`)
- Contains custom/override map definitions
- Defines region boundaries, names, and properties
- Supports both surface and underground areas
- Format matches RuneLite WorldMapDefinition structure

### Build Configuration
- **Maven** (`pom.xml`): Java build configuration with RuneLite dependencies
- **Checkstyle** (`checkstyle.xml`): Java code style enforcement
- **Requirements** (`requirements.txt`): Python dependencies

## Development Guidelines

### Adding New Maps
1. Add map definition to `user_world_defs.json` if needed
2. Ensure region coordinates are correct (verify in-game)
3. Test with debug map generation (`-1` fileId)
4. Validate output images and basemap definitions

### Working with Cache Data
- Always use the latest cache for accuracy
- Handle missing regions gracefully
- Validate XTEA keys before processing
- Cache large data structures to avoid repeated API calls

### Image Processing
- Use consistent tile sizes (64x64 pixels per game tile)
- Apply appropriate padding for map bounds
- Handle transparency and overlays correctly
- Optimize file sizes for web delivery

### Error Handling
- Log meaningful error messages with context
- Handle missing cache files gracefully
- Validate input coordinates and bounds
- Provide clear feedback on processing progress

## Testing & Validation

### Manual Testing
- Compare generated maps with in-game visuals
- Verify icon positions and types
- Check map boundaries and coordinates
- Test with different cache versions

### Automated Validation
- Validate JSON structure and required fields
- Check image dimensions and formats
- Verify file paths and naming conventions

## Dependencies & Setup

### Java Dependencies (via Maven)
- RuneLite cache library for OSRS data processing
- Google Gson for JSON handling
- SLF4J for logging

### Python Dependencies
- **numpy**: Numerical operations for image processing
- **Pillow**: Image manipulation and format handling
- **python-dateutil**: Date parsing for cache timestamps
- **requests**: HTTP requests for cache download

### Build Commands
```bash
# Install Python dependencies
pip3 install -r requirements.txt

# Build Java components
mvn clean compile

# Run the complete pipeline
python3 scripts/cache.py
mvn exec:java -Dexec.mainClass="wiki.runescape.oldschool.maps.MapExport"
python3 scripts/stitch.py
```

## CI/CD Integration

The project includes GitHub Actions workflow (`workflow-dispatch.yml`) for automated map generation:
- Supports manual triggering with runner selection
- Sets up JDK 11 and Python 3.12
- Caches Maven and pip dependencies
- Can be extended for automated deployments

## Output for OSRS Wiki

Generated files are designed for direct use on the OSRS Wiki:
- **Map Images**: High-quality PNG tiles for web display
- **Basemap Definitions**: JSON configuration for wiki map system
- **Icon Sprites**: Individual icon images for map overlays
- **Metadata**: Complete map definitions with coordinates and properties

Remember: This tool generates critical infrastructure for the OSRS Wiki map system. Accuracy and consistency are paramount, as these maps are used by thousands of players for navigation and reference.
