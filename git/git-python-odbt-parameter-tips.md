# GitPython `odbt` Parameter Tips

<!-- tl;dr starts -->

Sometimes, there are pieces of knowledge that is significant enough but too short to write into a proper TIL. This TIL is a collection of one-liner tips and tricks.

<!-- tl;dr ends -->

## `odbt=GitCmdObjectDB` versus `odbt=GitDB`

When connecting to GitHub Repository via GitPython, to choose proper `odbt=` parameter: Use `odbt=GitCmdObjectDB` when your application required maximum stability and reliability in exchange for a little overhead on time. Otherwise, use `odbt=GitDB` to achieve fastest running time. All Python projects I've created are using `odbt=GitDB`.
