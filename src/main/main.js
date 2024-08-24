
eval("let ele = document.getElementById('rag_chat');" + "\n"
  + "console.log(ele)" + "\n"
  + "if (ele) {" + "\n"
  + "ele.parentElement.style.flexGrow = '1'" + "\n"
  + "ele.parentElement.parentElement.style.flexGrow = '1'" + "\n"
  + "}" + "\n"
  + "Array.from(document.getElementsByClassName('show-api')).forEach(element => {" + "\n"
  + "element.parentElement.remove()" + "\n"
  + "})" + "\n"
  + "Array.from(document.getElementsByTagName('embed')).forEach(element => {" + "\n"
  + "element.style.height = '100%'" + "\n"
  + "element.parentElement.style.height = '100%'" + "\n"
  + "element.parentElement.parentElement.style.height = '100%'" + "\n"
  + "element.parentElement.parentElement.parentElement.style.flexGrow = '1'" + "\n"
  + "})" + "\n")


