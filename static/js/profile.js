document.addEventListener('DOMContentLoaded', function() {
    var textContainer = document.getElementById('upload-pic');
    textContainer.innerHTML = textContainer.innerHTML.replace('Currently: ', '');
    textContainer.innerHTML = textContainer.innerHTML.replace('Change:', '');
    // find the a  tags
    var aTags = textContainer.getElementsByTagName('a');
    // remove them
    while (aTags.length > 0) {
        aTags[0].parentNode.removeChild(aTags[0]);
    }
    // find the input tags and let them invisible
    var inputTags = textContainer.getElementsByTagName('input');
    for (var i = 0; i < inputTags.length; i++) {
        inputTags[i].style.display = 'none';
    }
});