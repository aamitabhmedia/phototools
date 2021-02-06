# -------------------------------------------------------
# Global variables
# -------------------------------------------------------
$CSVFileName = "exiftool_metadata.csv"
$CameraModelMissing = "MISSING"
$CameraModelOther = "OTHER"
$CameraModels = @{
    "NIKON D70" = "NIKD70"
    "NIKON D800" = "NIKD800"
    "HP PhotoSmart 618 (V1.10)" = "HP618"
    "HP PhotoSmart 618" = "HP618"
    "E950" = "E950"
    "Canon PowerShot S330" = "CANS330"
    "Canon PowerShot S45" = "CANS45"
    "Canon PowerShot S400" = "CANS400"
    "Canon PowerShot G2" = "CANG2"
    "C2ZD520ZC220Z" = "OLYC2Z"
    "DC210 Zoom (V05.00)" = "DC210"
    "Canon PowerShot A80" = "CANA80"
    "Canon EOS DIGITAL REBEL" = "CANRBL"
    "E4300" = "NIKE4300"
    "Canon EOS 5D" = "CAN5D"
    "Canon PowerShot S60" = "CANS60"
    "<Digimax S500 / Kenox S500 / Digimax Cyber 530>" = "SAMS500"
    "DigitalCAM" = "DigiCAM"
    "KODAK DX6490 ZOOM DIGITAL CAMERA" = "KODDX6490"
    "Canon PowerShot SD750" = "CANSD750"
    "Canon PowerShot SD870 IS" = "CANSD870"
    "Canon PowerShot SD1000" = "CANSD1000"
    "iPhone" = "iPhone"
    "SP560UZ" = "OLYSP560UZ"
    "Canon PowerShot SD850 IS" = "CANSD850"
    "Canon EOS DIGITAL REBEL XTi" = "CANXTi"
    "Canon EOS DIGITAL REBEL XSi" = "CANXSi"
    "Canon EOS 5D Mark II" = "CAN5DMkII"
    "NIKON D80" = "NIKD80"
    "NIKON D5000" = "NIKD5k"
    "BlackBerry 8330" = "BB8330"
    "Canon EOS REBEL T2i" = "CANT2i"
    "HDR-CX350V" = "HDRCX350V"
    "HDR-SR11" = "HDRSR11"
    "Canon PowerShot ELPH 300 HS" = "CAN300HS"
    "Canon EOS DIGITAL REBEL XT" = "CANXT"
    "Canon PowerShot SD1200 IS" = "CANSD1200"
    "HD2" = "GOPRHD2"
    "iPhone 5" = "iPhone5"
    "NIKON D5100" = "NIKD5100"
    "iPhone 5s" = "iPhone5s"
    "iPad 2" = "iPad2"
    "iPhone 6" = "iPhone6"
    "iPhone 6s Plus" = "iPhone6sp"
    "iPhone 6 Plus" = "iPhone6p"
    "iPhone SE" = "iPhoneSE"
}
$WordIgnoreList = {
    
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

    if (Test-Path $outfile) { Remove-Item $outfile; };
    $null | Out-File $outfile -Append -Encoding Ascii;

    Write-Host "Exporting to file $($outfile)" -ForegroundColor DarkCyan
    exiftool -q -csv -FileTypeExtension -MimeType -Model "$Folder" -ext jpg -ext nef -ext cr2 -ext png -ext mov -ext mp4 -ext avi > "$outfile"
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
    Write-Host "Importing from file $($outfile)" -ForegroundColor DarkCyan

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
function Get-IsImage {

    [CmdletBinding()]
    Param(
        [Parameter(Mandatory)]
        [string]$MimeType
    )

    if ("image" -eq $MimeType) {
        return $true
    }
    return $false
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

    $albumDesc = $AlbumName.Substring(11)
    $caption = $album_year + ' ' + $albumDesc

    return $caption
}

# -------------------------------------------------------
# Fix-Folder
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

    # Remove the trailing slash
    $Folder = $Folder.trim('\')

    $Files = Join-Path -Path $Folder -ChildPath "*"
    
    # Get album name from folder path
    $albumName = Split-Path $Folder -Leaf

    # derive caption and abbreviation from the album folder name
    $abbrev = Get-FolderAbbrev $albumName
    $Caption = Get-FolderCaption $albumName
    Write-Host "abbrev = $abbrev" -ForegroundColor Green
    Write-Host "caption = $Caption" -ForegroundColor Green

    if ($c) {
        Write-Host "---------------------------------------------" -ForegroundColor Cyan
        Write-Host "          Updating Caption" -ForegroundColor Cyan
        Write-Host " Caption: '$($Caption)'" -ForegroundColor Cyan
        Write-Host " $($Folder)" -ForegroundColor Cyan
        Write-Host "---------------------------------------------" -ForegroundColor Cyan

        if ($t) {
            Write-Host "Caption '$($Caption)' will be written to all the file" -ForegroundColor Green
        } else {

            try {
                exiftool.exe "-Description=$Caption" `
                    "-Title=$Caption" `
                    "-Subject=$Caption" `
                    "-Exif:ImageDescription=$Caption" `
                    "-iptc:ObjectName=$Caption" `
                    "-iptc:Caption-Abstract=$Caption" `
                    "-iptc:Headline=$Caption" `
                    -overwrite_original $Files
            } catch [Exception] {
                Write-Host "Error: Writing Caption" -ForegroundColor Red
                Write-Host $_.Exception -ForegroundColor Red
                Write-Host "----- D" -ForegroundColor Yellow
            }
        }
    }

    if ($r) {
        Write-Host "---------------------------------------------" -ForegroundColor Cyan
        Write-Host "            Renaming Files" -ForegroundColor Cyan
        Write-Host " Abbrev: '$($abbrev)'" -ForegroundColor Cyan
        Write-Host " $($Folder)" -ForegroundColor Cyan
        Write-Host "---------------------------------------------" -ForegroundColor Cyan
        Export-ImageMetadata $Folder
        $metadata = Import-ImageMetadata $Folder
        $metadata | Format-Table

        # if any of the Camera Model value is unknown then stop
        foreach ($record in $metadata) {
            if ($record.Model -eq $CameraModelMissing) {
                Write-Host "ERROR: Unknown Camera Model '$($record.ModelFull)' in album '$($Folder)'.  Aborting" -ForegroundColor Red
                return
            }
        }

        if ($t -ne $true) {

            # NOTES:
            # For improved performance see here: https://gist.github.com/ghotz/c614584f44bf975153ea
            # Helpful explanation of -stay_open: https://exiftool.org/forum/index.php?topic=4134.0
            # For MOV files use ffmpeg instead:
            #       ffmpeg -i input.mp4 -metadata:s:v rotate="180" -codec copy output.mp4

            # By Phil Harvey: https://exiftool.org/forum/index.php?topic=10672.0
            # For MOV/MP4, you may write native QuickTime tags or XMP.
            # But you will find that different software reads different types of metadata.
            # Perhaps a shotgun approach of writing something like XMP:Description,
            # UserData:Description, ItemList:Description and UserData:Description
            # could cover the bases.

            # Create an arguments file and initialize it
            # $argsfile = Join-Path -Path $env:TEMP -ChildPath "fix_caption_rename_exiftool_args.txt"
            # Write-Host "Args File Name = '$($argsfile)'"

            # if (Test-Path $argsfile) { Remove-Item $argsfile; };
            # $null | Out-File $argsfile -Append -Encoding Ascii;

            # Startup exiftool
            # Start-Process "exiftool" "-stay_open True -@ $argsfile";

            # loop through each image in the metadata array and send the command to args for it
            foreach ($record in $metadata) {

                $filepath = $record.Path
                $ext = $record.Ext
                $is_image = Get-IsImage($record.MimeType)
                $filesuffix = $abbrev + '_' + $record.Model

                # Write-Host "$filesuffix, path=$($record.Path)"
                Write-Host $filesuffix -NoNewline -ForegroundColor Green
                Write-Host ", $($record.Path)" -ForegroundColor White

                # send commands to rename the files based on the photo creation date
                # using the following template YYYYMMDD-HHmmSS-Snn_<abbrev>_<model>.ext
                if ($is_image -and $ext -eq "png") {
                    # "-d`n%Y%m%d_%H%M%S_%%.2c_$($filesuffix).%%le`n-filename<Xmp:DateCreated`n$($record.Path)`n" | Out-File $argsfile -Append -Encoding Ascii;
                    # "-execute`n" | Out-File $argsfile -Append -Encoding Ascii;
                    exiftool "-filename<DateCreated" -d "%Y%m%d_%H%M%S_%%.2c_$($filesuffix).%%le" -overwrite_original $filepath
                } else {
                    # "-d`n%Y%m%d_%H%M%S_%%.2c_$($filesuffix).%%le`n-filename<CreateDate`n$($record.Path)`n" | Out-File $argsfile -Append -Encoding Ascii;
                    # "-execute`n" | Out-File $argsfile -Append -Encoding Ascii;
                    exiftool "-filename<CreateDate" -d "%Y%m%d_%H%M%S_%%.2c_$($filesuffix).%%le" -overwrite_original $filepath
                }
            }

            # let the window stay open for a while... (or wait for a key)
            # Start-Sleep -s 5;

            # send command to shutdown
            # "-stay_open`nFalse`n" | Out-File $argsfile -Append -Encoding Ascii;

        }
    }
}

# -------------------------------------------------------
# Fix-FolderTree
# -------------------------------------------------------
function Fix-FolderTree {

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

    $dirs = Get-ChildItem -Directory $Folder
    
    foreach ($dir in $dirs) {
        Write-Host "-------------------------------------------------------------------" -ForegroundColor Magenta
        Write-Host "$($dir.FullName)" -ForegroundColor Magenta
        Write-Host "-------------------------------------------------------------------" -ForegroundColor Magenta
        Fix-Folder $dir.FullName -c:$c -r:$r -t:$t
    }
}

# -------------------------------------------------------
# Testing
# -------------------------------------------------------
# Import-ImageMetadata "C:\Users\ajmq\Downloads\exiftest\2040\2020-01-03 Mix of all Media Types"
# Fix-Folder $args[0]
# Fix-Folder "P:\pics\2040\2007-01-01 Mix Album with Big Name" -r
# Fix-FolderTree "P:\pics\2040\" -c -r
# Fix-Folder -c -r "P:\pics\2012\2012-02-14 Valentine's Day"
