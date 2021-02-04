function Get-FolderAbbrev {

    [CmdletBinding()]
    Param(
        [Parameter(Mandatory)]
        [string]$AlbumName
    )

    $splits = $AlbumName.Split(" ")
    $albumDate = $splits[0]
    $albumDesc = $splits[1..($splits.Count-1)]

    $datesplits = $albumDate.Split('-')
    if ($datesplits.Count -lt 3) {
        Write-Host "ERROR: Bad DATE format $($AlbumName)"
        return $null
    }
    $album_year = $datesplits[0]
    if ($album_year.length -lt 4) {
        Write-Host "ERROR: Bad YEAR format $($AlbumName)"
        return $null
    }
    $album_year_2digit = $album_year.Substring(2,2)
    $album_month = $datesplits[1]
    if ($album_month.length -lt 2) {
        Write-Host "ERROR: Bad MONTH format $($AlbumName)"
        return $null
    }
    $album_day = $datesplits[2]
    if ($album_day.length -lt 2) {
        Write-Host "ERROR: Bad DAY format $($AlbumName)"
        return $null
    }

    $abbrev = $null
    foreach ($word in $albumDesc) {
        $word = (Get-Culture).TextInfo.ToTitleCase($word)
        $wordabrv = $word.Substring(0,3)
        $abbrev += $wordabrv
    }

    $abbrev += $album_year_2digit

    return $abbrev
}

function Get-FolderCaption {

    [CmdletBinding()]
    Param(
        [Parameter(Mandatory)]
        [string]$AlbumName
    )

    $splits = $AlbumName.Split(" ")
    $albumDate = $splits[0]

    $datesplits = $albumDate.Split('-')
    if ($datesplits.Count -lt 3) {
        Write-Host "ERROR: Bad DATE format $($AlbumName)"
        return $null
    }
    $album_year = $datesplits[0]
    if ($album_year.length -lt 4) {
        Write-Host "ERROR: Bad YEAR format $($AlbumName)"
        return $null
    }
    $album_month = $datesplits[1]
    if ($album_month.length -lt 2) {
        Write-Host "ERROR: Bad MONTH format $($AlbumName)"
        return $null
    }
    $album_day = $datesplits[2]
    if ($album_day.length -lt 2) {
        Write-Host "ERROR: Bad DAY format $($AlbumName)"
        return $null
    }

    $abbrev = $null

    $albumDesc = $AlbumName.Substring(11)
    Write-Host "albumDesc = $albumDesc"

    $caption = $album_year + ' ' + $albumDesc

    return $caption
}

function Fix-Folder {

    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Folder
    )

    # Get album name from folder path
    $albumName = Split-Path $Folder -Leaf

    # derive caption and abbreviation from the album folder name
    $abbrev = Get-FolderAbbrev $albumName
    $caption = Get-FolderCaption $albumName
    Write-Host "abbrev = $abbrev"
    Write-Host "caption = $caption"

    exit

    try {
        exiftool.exe "-Description=$Caption" "-Title=$Caption" "-Subject=$Caption" `
            "-Exif:ImageDescription=$Caption" "-iptc:ObjectName=$Caption" `
            "-iptc:Caption-Abstract=$Caption" -overwrite_original $Files
    } catch {
        Write-Host "Error: Writing Caption"
    }

    $FileNamePattern = '-filename<${datetimeoriginal}_' + $Acronym + '%-c.%le'
    Write-Host "FileNamePattern = $FileNamePattern" -ForegroundColor Yellow
    exiftool '$FileNamePattern' -d '%Y%m%d_%H%M%S' -fileorder datetimeoriginal -overwrite_original $Files
}

Fix-Folder "2013-01-20 Nani's 70th Birthday"
# Fix-Folder "P:\pics\2013\2013-01-20 Nani's 70th Birthday\test" "2013-01-20 Nani's 70th Birthday" "*D800.NEF" "Na70thBd"
