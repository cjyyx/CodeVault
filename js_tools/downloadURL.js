function downloadURL(url) {
    /* 通过url下载 */
    var globalDocument = window.parent.document;
    var aEle = globalDocument.createElement('a');
    aEle.href = url;
    globalDocument.body.append(aEle);
    aEle.click();
}