// implement your own methods in here, if your data is coming from A rest API

import * as Files from './file'
import * as Post from './post'
export default {

  // post
  getPost: Post.getPost,

  // FIle
  getFile: Files.getFile,
  getFileMenu: Files.getFileMenu,

}
