class GEOTAG
{
    [string]$lat
    [string]$lon
    [string]$latref
    [string]$lonref

    GEOTAG ([string]$lat, [string]$lon, [string]$latref, [string]$lonref)
    {
        $this.lat = $lat
        $this.lon = $lon
        $this.latref = $latref
        $this.lonref = $lonref
    }
}

$CRYSTAL_GEOTAG = [GEOTAG]::New("37.650658", "-121.870626", "N", "W")
$PANDEY_GEOTAG = [GEOTAG]::New("37.64838977693133", "-121.8957291076366", "N", "W")
$DELHI_GEOTAG = [GEOTAG]::New("28.533837", "77.150540", "N", "E")
$DDUN_GEOTAG = [GEOTAG]::New("30.367110", "78.073360", "N", "E")

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
            [switch]$pandey=$false

    )

    $geotag = $null
    if ($crystal) { $geotag = $CRYSTAL_GEOTAG }
    elseif ($delhi) { $geotag = $DELHI_GEOTAG }
    elseif ($ddun) { $geotag = $DDUN_GEOTAG }
    elseif ($pandey) { $geotag = $PANDEY_GEOTAG }

    Fix-FolderGeotag -Folder $Folder `
        -lat $geotag.lat `
        -lon $geotag.lon `
        -latref $geotag.latref `
        -lonref $geotag.lonref
}

# -------------------------------------------------------
# Fix-FolderGeotagToHome
# -------------------------------------------------------
function Fix-FolderGeotagToHome {

    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true,
                    HelpMessage="Album Folder")]
        [string]$Folder
    )

    Fix-FolderGeotag -Folder $Folder `
        -lat $CRYSTAL_GEOTAG.lat `
        -lon $CRYSTAL_GEOTAG.lon `
        -latref $CRYSTAL_GEOTAG.latref `
        -lonref $CRYSTAL_GEOTAG.lonref
}

# -------------------------------------------------------
# Fix-FolderGeotagToDelhi
# -------------------------------------------------------
function Fix-FolderGeotagToDelhi {

    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true,
                    HelpMessage="Album Folder")]
        [string]$Folder
    )

    Fix-FolderGeotag -Folder $Folder `
        -lat $DELHI_GEOTAG.lat `
        -lon $DELHI_GEOTAG.lon `
        -latref $DELHI_GEOTAG.latref `
        -lonref $DELHI_GEOTAG.lonref
}

# -------------------------------------------------------
# Fix-FolderGeotag
# -------------------------------------------------------
function Fix-FolderGeotag {

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

        [Parameter(Mandatory=$false,
                    HelpMessage="Latitude ref value N|S")]
        [string]$latref="N",

        [Parameter(Mandatory=$false,
                    HelpMessage="Longitude ref value E|W")]
        [string]$lonref="W"
    )

    Write-Host "-------------------------------------------------------------------" -ForegroundColor Magenta
    Write-Host "$($Folder)" -ForegroundColor Magenta
    Write-Host "-------------------------------------------------------------------" -ForegroundColor Magenta

    Write-Host "Folder     = $Folder" -ForegroundColor Yellow
    Write-Host "Lat        = $lat" -ForegroundColor Yellow
    Write-Host "Lon        = $lon" -ForegroundColor Yellow
    Write-Host "Latref     = $latref" -ForegroundColor Yellow
    Write-Host "Lonref     = $lonref" -ForegroundColor Yellow

    # Remove the trailing slash
    $Folder = $Folder.trim('\')

    # $Files = Join-Path -Path $Folder -ChildPath "*"
    
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