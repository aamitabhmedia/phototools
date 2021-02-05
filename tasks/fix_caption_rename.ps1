# -------------------------------------------------------
# Global variables
# -------------------------------------------------------
$CSVFileName = "exif_cam_model.csv"
$CameraModelMissing = "MISSING"
$CameraModelOther = "OTHER"
$CameraModels = @{
    "Canon PowerShot ELPH 300 HS" = "ELPH300"
    "Canon EOS REBEL T2i" = "RBLT2i"
    "HD2" = "GOPRHD2"
    "iPad 2" = "iPad2"
    "Nikon D800" = "D800"
    "Nikon D70" = "D70"
}

# -------------------------------------------------------
# -------------------------------------------------------
function Get-CameraModelAbbrev {

    [CmdletBinding()]
    Param(
        [Parameter(Mandatory)]
        [string]$Model
    )

    $abbrev = $CameraModels[$Model]
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
        if ($null -ne $MimeType -or "" -ne $MimeType) {
            $MimeType = $MimeType.split('/')[0]
        }
        if ($null -eq $model -or "" -eq $model) {
            $model=""
            $abbrev = $CameraModelOther
        } else {
            $abbrev = Get-CameraModelAbbrev $model
        }
        $entry = [pscustomobject]@{
            Path=$SourceFile;
            Ext=$Ext;
            MimeType=$MimeType;
            Model=$abbrev;
            ModelFull=$model
        }
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
                    HelpMessage="Caption: Update caption in the images")]
         [switch]$c=$false,

         [Parameter(Mandatory=$false,
                    HelpMessage="Rename the images")]
         [switch]$r=$false,

         [Parameter(Mandatory=$false,
                    HelpMessage="Test only: Do not execute exiftool")]
         [switch]$t=$false
    )

    Write-Host "Folder     = $Folder" -ForegroundColor Yellow
    Write-Host "Caption    = $c" -ForegroundColor Yellow
    Write-Host "Rename     = $r" -ForegroundColor Yellow
    Write-Host "Test Only  = $t" -ForegroundColor Yellow

    $Files = Join-Path -Path $Folder -ChildPath "*"
    
    # Get album name from folder path
    $albumName = Split-Path $Folder -Leaf

    # derive caption and abbreviation from the album folder name
    $abbrev = Get-FolderAbbrev $albumName
    $Caption = Get-FolderCaption $albumName
    Write-Host "abbrev = $abbrev" -ForegroundColor Yellow
    Write-Host "caption = $Caption" -ForegroundColor Yellow

    if ($c) {
        Write-Host "------- Updating Caption --------" -ForegroundColor White
        return

        if ($t) {
            Write-Host "Caption '$($Caption)' will be written to all the file" -ForegroundColor Yellow
        } else {

            try {
                exiftool.exe "-Description=$Caption" "-Title=$Caption" "-Subject=$Caption" `
                    "-Exif:ImageDescription=$Caption" "-iptc:ObjectName=$Caption" `
                    "-iptc:Caption-Abstract=$Caption" -overwrite_original $Files
            } catch [Exception] {
                Write-Host "Error: Writing some Caption" -ForegroundColor Red
                Write-Host $_.Exception
            }
        }
    }

    if ($r) {
        Write-Host "------- Renaming Files --------" -ForegroundColor White
        Export-ImageMetadata $Folder
        $metadata = Import-ImageMetadata $Folder
        if ($t) {
            $metadata | Format-Table
        }

        # if any of the Camera Model value is unknown then stop
        foreach ($record in $metadata) {
            if ($record.Model -eq $CameraModelMissing) {
                Write-Host "ERROR: Unknown Camera Model '$($record.ModelFull)'.  Aborting RENAME" -ForegroundColor Red
                return
            }
        }

        if ($t -ne $true) {
            exiftool -ext jpg -ext nef -ext cr2 "-filename<`${datetimeoriginal}_$($abbrev)%-c.%le" -d '%Y%m%d_%H%M%S' -fileorder datetimeoriginal -overwrite_original $Files
            exiftool -ext png "-filename<`${XMP:DateCreated}_$($abbrev)%-c.%le" -d '%Y%m%d_%H%M%S' -fileorder XMP:DateCreated -overwrite_original $Files
            exiftool -ext mov "-filename<`${QuickTime:CreateDate}_$($abbrev)%-c.%le" -d '%Y%m%d_%H%M%S' -fileorder QuickTime:CreateDate -overwrite_original $Files
            exiftool -ext mp4 "-filename<`${Xmp:CreateDate}_$($abbrev)%-c.%le" -d '%Y%m%d_%H%M%S' -fileorder Xmp:CreateDate -overwrite_original $Files
        }
    }
}

# -------------------------------------------------------
# Testing
# -------------------------------------------------------
# Import-ImageMetadata "C:\Users\ajmq\Downloads\exiftest\2040\2020-01-03 Mix of all Media Types"
# Fix-Folder $args[0]
# Fix-Folder "P:\pics\2040\2007-01-01 Mix Album with Big Name" -nc
