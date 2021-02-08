class GEOTAG
{
    [string]$latlon
    [string]$latlonref

    GEOTAG ([string]$latlon, [string]$latlonref)
    {
        $this.latlon = $latlon
        $this.latlonref = $latlonref
    }
}

$CRYSTAL_GEOTAG = [GEOTAG]::New("37.650658, -121.870626", "NW")
$PANDEY_GEOTAG = [GEOTAG]::New("37.64838977693133, -121.8957291076366", "NW")
$DELHI_GEOTAG = [GEOTAG]::New("28.533837, 77.150540", "NE")
$DDUN_GEOTAG = [GEOTAG]::New("30.367110, 78.073360", "NE")
$SANGEETA_GEOTAG = [GEOTAG]::New("33.24661868110679, -111.8477148811208", "NE")

# -------------------------------------------------------
# Fix-FolderGeotagToHome
# -------------------------------------------------------
function Fix-FolderGeotagPreset {

    [CmdletBinding()]
    param(
            [Parameter(Mandatory=$true, HelpMessage="Album Folder")]
            [string]$Folder,

            [Parameter(Mandatory=$false, HelpMessage="HOME Geolocation")]
            [switch]$crystal=$false,

            [Parameter(Mandatory=$false, HelpMessage="DELHI Geolocation")]
            [switch]$delhi=$false,

            [Parameter(Mandatory=$false, HelpMessage="DEHRADUN Geolocation")]
            [switch]$ddun=$false,

            [Parameter(Mandatory=$false, HelpMessage="PANDEY Geolocation")]
            [switch]$pandey=$false,

            [Parameter(Mandatory=$false, HelpMessage="PANDEY Geolocation")]
            [switch]$pandeysangeeta=$false
    )

    $geotag = $null
    if ($crystal) { $geotag = $CRYSTAL_GEOTAG }
    elseif ($delhi) { $geotag = $DELHI_GEOTAG }
    elseif ($ddun) { $geotag = $DDUN_GEOTAG }
    elseif ($pandey) { $geotag = $PANDEY_GEOTAG }
    elseif ($sangeeta) { $geotag = $SANGEETA_GEOTAG }
    else {
        Write-Host "ERROR: Preset unknown.  Aborting" -ForegroundColor Red
        return
    }

    Fix-FolderGeotag -Folder $Folder `
        -latlon $geotag.latlon `
        -latlonref $geotag.latlonref
}

# -------------------------------------------------------
# Fix-FolderGeotag
# -------------------------------------------------------
function Fix-FolderGeotag {

    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true, HelpMessage="Album Folder")]
        [string]$Folder,

        [Parameter(Mandatory=$true, HelpMessage="Lat Lon comma separated value directly from google maps")]
        [string]$latlon,

        [Parameter(Mandatory=$false, HelpMessage="Latitude, Longitude ref value NW | SE")]
        [string]$latlonref="NW"
    )

    Write-Host "-------------------------------------------------------------------" -ForegroundColor Magenta
    Write-Host "$($Folder)" -ForegroundColor Magenta
    Write-Host "-------------------------------------------------------------------" -ForegroundColor Magenta

    Write-Host "Folder     = $Folder" -ForegroundColor Yellow
    Write-Host "latlon     = $latlon" -ForegroundColor Yellow
    Write-Host "latlonref  = $latlonref" -ForegroundColor Yellow

    # Remove the trailing slash
    $Folder = $Folder.trim('\')

    $splits = $latlon.Split(',')
    $lat = $splits[0].Trim()
    $lon = $splits[1].Trim()
    Write-Host "lat        = $lat" -ForegroundColor White
    Write-Host "lon        = $lon" -ForegroundColor White

    
    $latref = $latlonref.Substring(0,1)
    $lonref = $latlonref.Substring(1,1)
    Write-Host "latref     = $latref" -ForegroundColor White
    Write-Host "lonref     = $lonref" -ForegroundColor White

    exiftool "-GPSLatitude=$lat" "-GPSLongitude=$lon" "-GPSLatitudeRef=$latref" "-GPSLongitudeRef=$lonref" -overwrite_original $Folder
}

# -------------------------------------------------------
# Fix-FolderTreeGeotag
# -------------------------------------------------------
function Fix-FolderTreeGeotag {

    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true,
                    HelpMessage="Album Folder")]
        [string]$Folder,

        [Parameter(Mandatory=$true,
                    HelpMessage="Latitude to set")]
        [string]$lat,

        [Parameter(Mandatory=$true,
                    HelpMessage="Longitude to set")]
        [string]$lon,

        [Parameter(Mandatory=$true,
                    HelpMessage="Latitude ref value N|S")]
        [string]$latref,

        [Parameter(Mandatory=$true,
                    HelpMessage="Longitude ref value E|W")]
        [string]$lonref

    )

    Write-Host "Folder     = $Folder" -ForegroundColor Yellow
    Write-Host "Lat        = $lat" -ForegroundColor Yellow
    Write-Host "Lon        = $lon" -ForegroundColor Yellow
    Write-Host "Latref     = $latref" -ForegroundColor Yellow
    Write-Host "Lonref     = $lonref" -ForegroundColor Yellow

    Write-Host "ERROR: TOo Gangerous to implement.  Aboering" -ForegroundColor Red

    $dirs = Get-ChildItem -Directory $Folder
    
    foreach ($dir in $dirs) {
        Fix-FolderGeotag $dir.FullName -c:$c -r:$r -t:$t
    }
}

# -------------------------------------------------------
# Testing
# -------------------------------------------------------
# Fix-FolderGeotag "P:\pics\2040\2007-01-01 Mix Album with Big Name" 
# Fix-FolderTreeGeotag "P:\pics\2040\"
# Fix-FolderGeotag "P:\pics\2012\2012-02-14 Valentine's Day"