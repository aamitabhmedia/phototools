# -------------------------------------------------------
# Global variables
# -------------------------------------------------------
$CSVFileName = "exif_cam_model.csv"
$CameraModelMissing = "MISSING"
$CameraModelOther = "OTHER"

# -------------------------------------------------------
# -------------------------------------------------------
function Get-CameraModelAbbrev {

    [CmdletBinding()]
    Param(
        [Parameter(Mandatory)]
        [string]$Model
    )

    $abbrevs = @{
        "Nikon D800" = "D800"
        "Nikon D70" = "D70"
    }

    $abbrev = $abbrevs[$Model]
    if ($null -eq $abbrev) {
        $abbrev = "MISSING"
    }

    return $abbrev
}

# -------------------------------------------------------
# -------------------------------------------------------
function Get-ImageMetadataCsvPath {
    [CmdletBinding()]
    Param(
        [Parameter(Mandatory)]
        [string]$Folder
    )

    return Join-Path -Path $Folder -ChildPath $CSVFileName
}

# -------------------------------------------------------
# -------------------------------------------------------
function Export-ImageMetadata {
    [CmdletBinding()]
    Param(
        [Parameter(Mandatory)]
        [string]$Folder
    )

    $outfile = Get-ImageMetadataCsvPath $Folder
    exiftool -csv -FileTypeExtension -MimeType -Model "$Folder" -ext jpg -ext nef -ext cr2 -ext png -ext mov -ext mp4 -ext avi > "$outfile"
}

# -------------------------------------------------------
# -------------------------------------------------------
function Import-ImageMetadata {
    [CmdletBinding()]
    Param(
        [Parameter(Mandatory)]
        [string]$Folder
    )

    $outfile = Get-ImageMetadataCsvPath $Folder
    $csvresult = Import-Csv "$outfile"

    $metadata = @()
    $csvresult | ForEach-Object {
        $abbrev = $null
        $SourceFile = $_.SourceFile
        $model = $_.Model
        $Ext=$_.FileTypeExtension
        $MimeType=$_.MimeType
        if ($null -eq $model -or "" -eq $model) {
            $abbrev = $CameraModelOther
        } else {
            $abbrev = Get-CameraModelAbbrev $model
        }
        $entry = [pscustomobject]@{Path=$SourceFile; Ext=$Ext; MimeType=$MimeType; Model=$abbrev}
        $metadata += $entry
    }

    return $metadata
}

# -------------------------------------------------------
# -------------------------------------------------------
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
        $wordabrv = $word
        if ($word.Length -gt 3) {
            $wordabrv = $word.Substring(0,3)
        }
        $abbrev += $wordabrv
    }

    $abbrev += $album_year_2digit

    return $abbrev
}

# -------------------------------------------------------
# -------------------------------------------------------
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

# -------------------------------------------------------
# -------------------------------------------------------
function Fix-Folder {

    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true,
                    HelpMessage="Album Folder")]
        [string]$Folder,

        [Parameter(Mandatory=$false,
                    HelpMessage="No Caption: DO not add caption to the images")]
         [switch]$nc=$false,

         [Parameter(Mandatory=$false,
                    HelpMessage="No Rename: Do not rename the files")]
         [switch]$nr=$false,

         [Parameter(Mandatory=$false,
                    HelpMessage="Test only: Do not execute exiftool")]
         [switch]$t=$false
    )

    Write-Host "Folder     = $Folder" -ForegroundColor Yellow
    Write-Host "No Caption = $nc" -ForegroundColor Yellow
    Write-Host "No Rename  = $nr" -ForegroundColor Yellow
    Write-Host "Test Only  = $t" -ForegroundColor Yellow

    $Files = Join-Path -Path $Folder -ChildPath "*"
    
    # Get album name from folder path
    $albumName = Split-Path $Folder -Leaf

    # derive caption and abbreviation from the album folder name
    $abbrev = Get-FolderAbbrev $albumName
    $Caption = Get-FolderCaption $albumName
    Write-Host "abbrev = $abbrev" -ForegroundColor Yellow
    Write-Host "caption = $Caption" -ForegroundColor Yellow

    if ($nc -eq $false) {
        Write-Host "nc" -ForegroundColor White
        try {
            exiftool.exe "-Description=$Caption" "-Title=$Caption" "-Subject=$Caption" `
                "-Exif:ImageDescription=$Caption" "-iptc:ObjectName=$Caption" `
                "-iptc:Caption-Abstract=$Caption" -overwrite_original $Files
        } catch [Exception] {
            Write-Host "Error: Writing some Caption"
            Write-Host $_.Exception
        }
    }

    if ($nr -eq $false) {
        Write-Host "nr" -ForegroundColor White
        Export-ImageMetadata $Folder
        $metadata = Import-ImageMetadata $Folder
        Write-Host $metadata -ForegroundColor White
        return
        exiftool -ext jpg -ext nef -ext cr2 "-filename<`${datetimeoriginal}_$($abbrev)%-c.%le" -d '%Y%m%d_%H%M%S' -fileorder datetimeoriginal -overwrite_original $Files
        exiftool -ext png "-filename<`${XMP:DateCreated}_$($abbrev)%-c.%le" -d '%Y%m%d_%H%M%S' -fileorder XMP:DateCreated -overwrite_original $Files
        exiftool -ext mov "-filename<`${QuickTime:CreateDate}_$($abbrev)%-c.%le" -d '%Y%m%d_%H%M%S' -fileorder QuickTime:CreateDate -overwrite_original $Files
        exiftool -ext mp4 "-filename<`${Xmp:CreateDate}_$($abbrev)%-c.%le" -d '%Y%m%d_%H%M%S' -fileorder Xmp:CreateDate -overwrite_original $Files
    }
}

# -------------------------------------------------------
# Testing
# -------------------------------------------------------
# Import-ImageMetadata "C:\Users\ajmq\Downloads\exiftest\2040\2020-01-03 Mix of all Media Types"
# Fix-Folder $args[0]
Fix-Folder "P:\pics\2040\2007-01-01 Mix Album with Big Name" -nc
