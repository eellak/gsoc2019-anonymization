selected_word = null
words_to_be_anonymized = []
$(document).ready(function () {
    $("#anonymized_text").click(function () {
        // Get word
        word = window.getSelection().toString();
        if (word != '') {
            selected_word = word;
            fade();
            document.getElementById('anonymize_word_button').style.opacity = 1;

        }
    });
});

function fade() {
    var i = 0;
    var h1 = document.getElementById("anonymize_word_button");
    h1.style.opacity = 0.5;
    var k = window.setInterval(function () {
        if (i >= 10) {
            clearInterval(k);
        } else {
            h1.style.opacity = i / 10;
            i++;
        }
    }, 100);

};


function addWordsToBeAnonymized() {
    if (selected_word != null) {
        words_to_be_anonymized.push(selected_word)
    }
    console.log(words_to_be_anonymized)
    // Document.activeElement.style.opacity = 0;
    window.getSelection().empty();

}

function updateText() {
    base_url = window.location.href.split('?')[0]
    // console.log(base_url)
    new_url = base_url + '?param=' + JSON.stringify(words_to_be_anonymized);
    window.location = new_url;
}

function deleteWordsToBeAnonymized(n) {
    if (n == -1) {
        words_to_be_anonymized = [];
        base_url = window.location.href.split('?')[0]
        // console.log(base_url)
        new_url = base_url;
        window.location = new_url;

    }
    else if (n > -1) {
        words_to_be_anonymized.splice(n, 1);
    }
    else {
        console.log('Error not valid number of deleteWordsToBeAnonymized array');
    }
};



