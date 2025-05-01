# JPG, JPEG, JFIF

<!-- tl;dr starts -->

**JPEG** is the name of an ISO's subcommittee (Joint Photographic Expert Group) that helped create a lossy compression algorithm that results in significant smaller file sizes with little to no perceptible impact on picture quality and resolution. It's also a standardized file extension, `.jpeg`.

**JPG** is actually the shorten version of `.jpeg` in terms of file extension, due to the limitation of file format maximum length in old versions of Windows and Unix.

**JFIF** is the _file format_ that uses the JPEG compression algorithm, developed by Eric Hamilton at C-Cube Microsystems.

<!-- tl;dr ends -->

## File extension

The original _file extension_ for the Joint Photographic Expert Group _file format_ was `.jpeg`, but it all came to Unix to blame for this. In the old versions of Windows whose most programs had to cope with DOS 8.3, all files required an exact three and only three letter file extension, so it got shorten to `.jpg`. Mac and GNU/Linux OS don't have this restriction so they chose `.jpeg`. Later versions of Windows have lifted the restriction and `.jpeg` was acceptable. However since so many users have get accustomed to using `.jpg`, it still is the most commonly accepted and used file extension.

> Adobe Photoshop save all JPEG files with a `.jpg` file extension on both Mac and Windows.
> Uppercase is acceptable. `.JPEG` or `.JPG`

There are 6 different standardized file name extensions that're all corresponded to JPEG images. The first two are the most common, last four are less common

- `.jpg`
- `.jpeg`
- `.jpe`
- `.jif`
- `.jfif`
- `.jfi`

## Compression algorithm

JPEG is a method for lossy compression of digital images, it defines how image data is compressed to reduce file size by ten times while maintaining acceptable visual quality. It specifies the _encoding process_ but not _how the compressed data should be stored_.

## File format

JFIF is a file format that uses JPEG compression algorithm. It defines how to store that compressed data in a file on an operating system. When someone mention a JPEG file or JPG file (remember, only different in file extension naming), they're talking about JPEG/JFIF file.

Technical aspects:

- It adds specific metadata like resolution information, ...
- It has a specific file signature. Example: JPEG/JFIF file, ISO 8859-1 `FF D8 FF E0 JFIF`
  > More file signatures can be found at [Gary Kessler's List of File Signatures](https://www.garykessler.net/library/file_sigs.html).
- It standardizes color spaces and component sampling.

However, there are other alternative file formats such as JPEG/EXIF, JPEG/CIFF, JPEG/SPIFF ... that also use JPEG compression algorithm but store data differently.
