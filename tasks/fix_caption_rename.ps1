# -------------------------------------------------------
# TODO:
# 1. Enhance the caption update -c option as follows
#       If images does not have caption then add caption
#       by using the album name and its year
#
#       If caption is aready there and it does not have
#       the album year prefix then add it
#
#       if captions are different in the folder then
#       issue an error unless a -force switch is used
# -------------------------------------------------------

# -------------------------------------------------------
# Global variables
# -------------------------------------------------------
$CSVFileName = "exiftool_metadata.csv"
$ExiftoolCaptionArgsFile = "exiftool_caption_args.txt"
$ExiftoolRenameArgsFile = "exiftool_rename_args.txt"
$CameraModelMissing = "MISSING"
$CameraModelOther = "OTHER"
$CameraModels = @{
    "NIKON D70" = "NIKD70"
    "NIKON D800" = "NIKD800"
    "Nikon COOLSCAN V ED" = "NIKCOOLSCANVED"
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
    "iPad 2" = "iPad2"
    "iPhone 5" = "iPhone5"
    "iPhone 5s" = "iPhone5s"
    "iPhone 6" = "iPhone6"
    "iPhone 6s Plus" = "iPhone6sp"
    "iPhone 6 Plus" = "iPhone6p"
    "iPhone SE" = "iPhoneSE"
    "iPhone X" = "iPhoneX"
    "NIKON D5100" = "NIKD5100"
    "SCANNER" = "SCANNER"
}

$WordShortenList = @{
    "And" = "Nd"
    "Day" = "Dy"
    "New" = "Nw"
    "Big" = "Bg"
    "San" = "Sn"
    "Gap" = "Gp"
    "For" = "Fr"
    "All" = "Al"
    "The" = "Th"
    "Fun" = "Fn"
    "Eve" = "Ev"
    "Las" = "Ls"
    "Off" = "Of"
    "Bad" = "Bd"
    "Mix" = "Mx"
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
    exiftool -q -csv `
    "-FileTypeExtension" `
    "-MimeType" `
    "-Model" `
    "-Description" `
    "-iptc:Caption-Abstract" `
    "-iptc:ObjectName" `
    "-Title" `
    "-Exif:ImageDescription" `
    "-Subject" `
    "-iptc:Headline" `
    -ext jpg -ext nef -ext cr2 -ext png -ext mov -ext mp4 -ext avi `
    "$Folder" > "$outfile"
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

    $records = Import-Csv "$outfile"

    foreach ($record in $records) {
        $mimeType = $record.MimeType
        if ($null -ne $mimeType -or "" -ne $mimeType) {
            $record.MimeType = $mimeType.split('/')[0]
        }

        $model = $record.Model
        if ($null -eq $model -or "" -eq $model) {
            $record.Model = $CameraModelOther
        } else {
            $record.Model = Get-CameraModelAbbrev $model
        }
    }

    return [PSCustomObject]$records
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
        $word = $word.Replace("'", '')
        $word = $word.Replace(".", '')
        $word = $word.Replace(",", '')
        $word = $word.Replace("-", '')

        $wordabrv = $word

        if ($word.Length -eq 3 -and $word -eq "The") {
            $wordabrv = "Th"
        }
        elseif ($word.Length -gt 3) {
            $wordabrv = $word.Substring(0,3)
        }
        else {
            $wordshort = $WordShortenList[$word]
            if ($null -ne $wordshort) {
                $wordabrv = $wordshort
            }
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
function Split-AlbumNameToCaptionComponents {

    [CmdletBinding()]
    Param(
        [Parameter(Mandatory)]
        [string]$AlbumName
    )

    if ($AlbumName.Length -lt 12) {
        Write-Host "ERROR: Album too short to contain YEAR $($AlbumName)"
        return $null
    }

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

    return [ordered] @{
        year = $album_year;
        month = $album_month;
        day = $album_day;
        desc = $albumDesc
    }
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
# Get-AnyCaption
# -------------------------------------------------------
function Get-AnyCaption {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true, HelpMessage="A CSV record of caption tags")]
        [PSCustomObject]$record
    )

    $isImage = Get-IsImage($record.MimeType)

    $caption = $null

    if ($isImage) {
        if ($record.Description.Length -gt 0) {
            $caption = $record.Description
        }
        elseif ($null -eq $caption -and $record.'Caption-Abstract'.Length -gt 0) {
            $caption = $record.'Caption-Abstract'
        }
        elseif ($null -eq $caption -and $record.ObjectName.Length -gt 0) {
            $caption = $record.ObjectName
        }
        elseif ($null -eq $caption -and $record.Title.Length -gt 0) {
            $caption = $record.Title
        }
        elseif ($null -eq $caption -and $record.ImageDescription.Length -gt 0) {
            $caption = $record.ImageDescription
        }
        elseif ($null -eq $caption -and $record.Headline.Length -gt 0) {
            $caption = $record.Headline
        }
        elseif ($null -eq $caption -and $record.Subject.Length -gt 0) {
            $caption = $record.Subject
        }
    }
    else {
        if ($null -eq $caption -and $record.Title.Length -gt 0) {
            $caption = $record.Title
        }
        elseif ($record.Description.Length -gt 0) {
            $caption = $record.Description
        }
        elseif ($null -eq $caption -and $record.'Caption-Abstract'.Length -gt 0) {
            $caption = $record.'Caption-Abstract'
        }
        elseif ($null -eq $caption -and $record.ObjectName.Length -gt 0) {
            $caption = $record.ObjectName
        }
        elseif ($null -eq $caption -and $record.ImageDescription.Length -gt 0) {
            $caption = $record.ImageDescription
        }
        elseif ($null -eq $caption -and $record.Headline.Length -gt 0) {
            $caption = $record.Headline
        }
        elseif ($null -eq $caption -and $record.Subject.Length -gt 0) {
            $caption = $record.Subject
        }
    }

    return $caption
}


# -------------------------------------------------------
# -------------------------------------------------------
function Get-PFilmPattern {

    [CmdletBinding()]
    Param(
        [Parameter(Mandatory)]
        [string]$ImageFileName
    )

    $idx = $ImageFileName.IndexOf("PFILM")
    if ($idx -lt 0) {
        return $null
    }

    $sub = $ImageFileName.substring($idx, 12)
    return $sub
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
                    HelpMessage="Force album name to caption of all images")]
         [switch]$f=$false,

         [Parameter(Mandatory=$false,
                    HelpMessage="Rename the images")]
         [switch]$r=$false,

         [Parameter(Mandatory=$false,
                    HelpMessage="Test only: Do not execute exiftool")]
         [switch]$t=$false,

         [Parameter(Mandatory=$false,
                    HelpMessage="Verbose")]
         [switch]$v=$false
    )

    Write-Host "-------------------------------------------------------------------" -ForegroundColor Magenta
    Write-Host "$($Folder)" -ForegroundColor Magenta
    Write-Host "-------------------------------------------------------------------" -ForegroundColor Magenta

    Write-Host "Folder     = $Folder" -ForegroundColor Yellow
    Write-Host "Caption    = $c" -ForegroundColor Yellow
    Write-Host "Force      = $f" -ForegroundColor Yellow
    Write-Host "Rename     = $r" -ForegroundColor Yellow
    Write-Host "Test Only  = $t" -ForegroundColor Yellow

    # Remove the trailing slash
    $Folder = $Folder.trim('\')
    
    # Get album name from folder path
    $albumName = Split-Path $Folder -Leaf

    # derive caption and abbreviation from the album folder name
    $abbrev = Get-FolderAbbrev $albumName
    $folderCaption = Get-FolderCaption $albumName
    $albumNameCaptionComponents = Split-AlbumNameToCaptionComponents $albumName

    Write-Host "abbrev = $abbrev" -ForegroundColor Green
    Write-Host "caption = $folderCaption" -ForegroundColor Green
    Write-Host "components:" -ForegroundColor Green
    Write-Host "     year: '$($albumNameCaptionComponents.year)'" -ForegroundColor Green
    Write-Host "    month: '$($albumNameCaptionComponents.month)'" -ForegroundColor Green
    Write-Host "      day: '$($albumNameCaptionComponents.day)'" -ForegroundColor Green
    Write-Host "     desc: '$($albumNameCaptionComponents.desc)'" -ForegroundColor Green

    # build a file of metadata of all images and videos in this folder
    Export-ImageMetadata $Folder
    $records = Import-ImageMetadata $Folder
    Write-Host "Record Count = $($records.Length)" -ForegroundColor Magenta

    if ($c) {
        Write-Host "---------------------------------------------" -ForegroundColor Cyan
        Write-Host "          Updating Caption" -ForegroundColor Cyan
        Write-Host " Folder Caption: '$($folderCaption)'" -ForegroundColor Cyan
        Write-Host " $($Folder)" -ForegroundColor Cyan
        Write-Host "---------------------------------------------" -ForegroundColor Cyan

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

        $result = @()

        # Loop through each record
        foreach ($record in $records) {

            $isImage = Get-IsImage($record.MimeType)

            if ($v) {
                Write-Host "File: $($record.SourceFile)" -ForegroundColor Yellow
                Write-Host "    Description: $($record.Description)"
                Write-Host "    ObjectName: $($record.ObjectName)"
                Write-Host "    Caption-Abstract: $($record.'Caption-Abstract')"
                Write-Host "    Title: $($record.Title)"
                Write-Host "    ImageDescription: $($record.ImageDescription)"
                Write-Host "    Headline: $($record.Headline)"
                Write-Host "    Subject: $($record.Subject)"
                Write-Host "    FileTypeExtension: $($record.FileTypeExtension)"
                Write-Host "    MimeType: $($record.MimeType)"
                Write-Host "    Model: $($record.Model)"
                Write-Host "    IsImage: $($isImage)"
            }

            $caption = Get-AnyCaption $record

            $newCaption = $caption

            # If caption does not exist on the images then use the caption from the album
            if ($f -or $null -eq $caption) {
                $newCaption = $folderCaption
            }

            # Check if caption already has year as prefix
            else {
                $caption_year = $null
                if ($caption.Length -gt 6) {
                    $caption_year = $caption.Substring(0, 4)

                    # Does not have year prefix then add year
                    if (-not ($caption_year -match "^\d+$")) {
                        $newCaption = $albumNameCaptionComponents.year + ' ' + $caption
                    }
                }

                # Caption cannot have year in it. Assume text and add prefix
                else {
                    $newCaption = $albumNameCaptionComponents.year + ' ' + $caption
                }
            }

            # new caption different from image caption.  Update Image caption
            if ($caption -ne $newCaption) {
                Write-Host "File = $($record.SourceFile)" -ForegroundColor Green
                Write-Host "    cur caption = '$($caption)'" -ForegroundColor Green
                Write-Host "    new caption = '$($newCaption)'" -ForegroundColor Green

                $result_record = @{
                    SourceFile = $record.SourceFile;
                    CurrCaption = $caption;
                    NewCaption = $newCaption;
                    IsImage = $isImage;
                    Ext = $record.FileTypeExtension
                }
                $result += $result_record
            }
        }

        # loop through the result and write the tags
        if ($result.Count -gt 0) {

            # Create an arguments file and initialize it
            $argsfile = Join-Path -Path $Folder -ChildPath $ExiftoolCaptionArgsFile
            Write-Host "Args File Name = '$($argsfile)'"

            if (Test-Path $argsfile) { Remove-Item $argsfile; };
            $null | Out-File $argsfile -Append -Encoding Ascii;

            # send stay open command
            "-stay_open`nTrue`n" | Out-File $argsfile -Append -Encoding Ascii;

            foreach ($result_record in $result) {

                Write-Host "File: '$($result_record.SourceFile)'" -ForegroundColor Cyan
                Write-Host "    Curr Caption: '$($result_record.CurrCaption)'" -ForegroundColor Cyan
                Write-Host "     New Caption: '$($result_record.NewCaption)'" -ForegroundColor Cyan
                Write-Host "        is_image: '$($result_record.IsImage)'" -ForegroundColor Cyan
                Write-Host "       Extension: '$($result_record.Ext)'" -ForegroundColor Cyan

                $isImage = $result_record.IsImage
                $ext = $result_record.Ext

                # Update image
                if ($isImage) {
                    if ("png" -eq $ext) {
                        "-Description=$($result_record.NewCaption)" | Out-File $argsfile -Append -Encoding Ascii;
                        "-Title=$($result_record.NewCaption)" | Out-File $argsfile -Append -Encoding Ascii;
                        "-Exif:ImageDescription=$($result_record.NewCaption)" | Out-File $argsfile -Append -Encoding Ascii;
                        "-Subject=$($result_record.NewCaption)" | Out-File $argsfile -Append -Encoding Ascii;
                        "-ext`npng" | Out-File $argsfile -Append -Encoding Ascii;
                    }
                    else {
                        "-Description=$($result_record.NewCaption)" | Out-File $argsfile -Append -Encoding Ascii;
                        "-iptc:Caption-Abstract=$($result_record.NewCaption)" | Out-File $argsfile -Append -Encoding Ascii;
                        "-iptc:ObjectName=$($result_record.NewCaption)" | Out-File $argsfile -Append -Encoding Ascii;
                        "-iptc:Headline=$($result_record.NewCaption)" | Out-File $argsfile -Append -Encoding Ascii;
                        "-Exif:ImageDescription=$($result_record.NewCaption)" | Out-File $argsfile -Append -Encoding Ascii;
                        "-Title=$($result_record.NewCaption)" | Out-File $argsfile -Append -Encoding Ascii;
                        "-ext`nnef`n-ext`njpg`n-ext`ncr2" | Out-File $argsfile -Append -Encoding Ascii;
                    }
                }

                # Update Video
                else {
                    "-QuickTime:Title=$($result_record.NewCaption)" | Out-File $argsfile -Append -Encoding Ascii;
                    "-Description=$($result_record.NewCaption)" | Out-File $argsfile -Append -Encoding Ascii;
                    "-iptc:Caption-Abstract=$($result_record.NewCaption)" | Out-File $argsfile -Append -Encoding Ascii;
                    "-iptc:ObjectName=$($result_record.NewCaption)" | Out-File $argsfile -Append -Encoding Ascii;
                    "-iptc:Headline=$($result_record.NewCaption)" | Out-File $argsfile -Append -Encoding Ascii;
                    "-Exif:ImageDescription=$($result_record.NewCaption)" | Out-File $argsfile -Append -Encoding Ascii;
                    "-Subject=$($result_record.NewCaption)" | Out-File $argsfile -Append -Encoding Ascii;
                    "-ext`nmov`n-ext`nmp4`n-ext`navi" | Out-File $argsfile -Append -Encoding Ascii;
                }

                "-overwrite_original" | Out-File $argsfile -Append -Encoding Ascii;
                "$($result_record.SourceFile)" | Out-File $argsfile -Append -Encoding Ascii;
                "-execute`n" | Out-File $argsfile -Append -Encoding Ascii;
            }

            # send shutdown command, and run the batch file
            "-stay_open`nFalse`n" | Out-File $argsfile -Append -Encoding Ascii;
            exiftool -@ $argsfile
        }
    }

    if ($r) {
        Write-Host "---------------------------------------------" -ForegroundColor Cyan
        Write-Host "            Renaming Files" -ForegroundColor Cyan
        Write-Host " Abbrev: '$($abbrev)'" -ForegroundColor Cyan
        Write-Host " $($Folder)" -ForegroundColor Cyan
        Write-Host "---------------------------------------------" -ForegroundColor Cyan
        # Export-ImageMetadata $Folder
        # $records = Import-ImageMetadata $Folder
        # $records | Format-Table

        # if any of the Camera Model value is unknown then stop
        foreach ($record in $records) {
            if ($record.Model -eq $CameraModelMissing) {
                Write-Host "ERROR: Unknown Camera Model '$($record.ModelFull)' in album '$($Folder)'.  Aborting" -ForegroundColor Red
                return
            }
        }

        # Create an arguments file and initialize it
        $argsfile = Join-Path -Path $Folder -ChildPath $ExiftoolRenameArgsFile
        Write-Host "Args File Name = '$($argsfile)'"

        if (Test-Path $argsfile) { Remove-Item $argsfile; };
        $null | Out-File $argsfile -Append -Encoding Ascii;

        # send stay open command
        "-stay_open`nTrue`n" | Out-File $argsfile -Append -Encoding Ascii;

        # loop through each image in the metadata array and send the command to args for it
        foreach ($record in $records) {

            $isImage = Get-IsImage($record.MimeType)
            $pfilmPattern = $null
            $ext = $record.FileTypeExtension
            if ($isImage -and ($ext -eq "jpg" -or $ext -eq "jpeg")) {
                $pfilmPattern = Get-PFilmPattern($record.SourceFile)
            }
            $filesuffix = $abbrev + '_' + $record.Model
            if ($null -ne $pfilmPattern) {
                $filesuffix = $abbrev + '_' + $record.Model + '_' + $pfilmPattern
            }

            # Write-Host "$filesuffix, path=$($record.SourceFile)"
            Write-Host $filesuffix -NoNewline -ForegroundColor Green
            Write-Host ", $($record.SourceFile)" -ForegroundColor White

            # send commands to rename the files based on the photo creation date
            # using the following template YYYYMMDD-HHmmSS-Snn_<abbrev>_<model>.ext
            if ($isImage -and $ext -ne "png") {
                "-d`n%Y%m%d_%H%M%S_%%.2c_$($filesuffix).%%le`n-filename<DateTimeOriginal`n$($record.SourceFile)" | Out-File $argsfile -Append -Encoding Ascii;
                "-execute`n" | Out-File $argsfile -Append -Encoding Ascii;
                # exiftool "-filename<DateCreated" -d "%Y%m%d_%H%M%S_%%.2c_$($filesuffix).%%le" -overwrite_original $filepath
            }
            elseif ($isImage -and $ext -eq "png") {
                "-d`n%Y%m%d_%H%M%S_%%.2c_$($filesuffix).%%le`n-filename<Xmp:DateCreated`n$($record.SourceFile)" | Out-File $argsfile -Append -Encoding Ascii;
                "-execute`n" | Out-File $argsfile -Append -Encoding Ascii;
                # exiftool "-filename<DateCreated" -d "%Y%m%d_%H%M%S_%%.2c_$($filesuffix).%%le" -overwrite_original $filepath
            } else {
                "-d`n%Y%m%d_%H%M%S_%%.2c_$($filesuffix).%%le`n-filename<CreateDate`n$($record.SourceFile)" | Out-File $argsfile -Append -Encoding Ascii;
                "-execute`n" | Out-File $argsfile -Append -Encoding Ascii;
                # exiftool "-filename<CreateDate" -d "%Y%m%d_%H%M%S_%%.2c_$($filesuffix).%%le" -overwrite_original $filepath
            }
        }

        # send shutdown command
        "-stay_open`nFalse`n" | Out-File $argsfile -Append -Encoding Ascii;

        # Run the exiftool in batch mode
        if (-not $t) {
            exiftool -@ $argsfile
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
                    HelpMessage="Force album name to caption of all images")]
         [switch]$f=$false,

         [Parameter(Mandatory=$false,
                    HelpMessage="Rename the images")]
         [switch]$r=$false,

         [Parameter(Mandatory=$false,
                    HelpMessage="Test only: Do not execute exiftool")]
         [switch]$t=$false
    )

    Write-Host "Folder        = $Folder" -ForegroundColor Yellow
    Write-Host "Caption       = $c" -ForegroundColor Yellow
    Write-Host "Force Caption = $f" -ForegroundColor Yellow
    Write-Host "Rename        = $r" -ForegroundColor Yellow
    Write-Host "Test Only     = $t" -ForegroundColor Yellow

    $dirs = Get-ChildItem -Directory $Folder

    if ($f -eq $true) {
        $confirmation = Read-Host "Force flag specified. Are you Sure You Want To Proceed:"
        if ($confirmation -ne 'y') {
            Write-Host "Aborting"
            return
        }
    }

    foreach ($dir in $dirs) {
        Fix-Folder $dir.FullName -c:$c -f:$f -r:$r -t:$t
    }
}

# -------------------------------------------------------
# Testing
# -------------------------------------------------------
# Fix-Folder -r "P:\pics\2040\2007-01-01 Mix Album with Big Name"
# Import-ImageMetadata "C:\Users\ajmq\Downloads\exiftest\2040\2020-01-03 Mix of all Media Types"
# Fix-Folder -c "P:\pics\2040\2007-01-01 Mix Album with Big Name"
# Fix-Folder $args[0]
# Fix-Folder "P:\pics\2040\2007-01-01 Mix Album with Big Name" -r
# Fix-FolderTree "P:\pics\2040\" -c -r
# Fix-Folder -c -r "P:\pics\2012\2012-02-14 Valentine's Day"
Fix-Folder -c -r "D:\Downloads\1994-03-01 Ishika Ranodom Pics\"
