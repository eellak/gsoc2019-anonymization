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
$(document).ready(function () {
    $("#original_document").click(function () {
        // Get word
        word = window.getSelection().toString();
        if (word != '') {
            selected_word = word;
            fade();
            document.getElementById('anonymize_word_button').style.opacity = 1;

        }
    });
});

$(document).ready(function () {
    $("#anonymized_document").click(function () {
        // Get word
        word = window.getSelection().toString();
        if (word != '') {
            selected_word = word;
            fade();
            document.getElementById('anonymize_word_button').style.opacity = 1;

        }
    });
});

function reload() {
    base_url = window.location.href.split('?')[0]
    // console.log(base_url)
    new_url = base_url + '?reload=True';
    words_to_be_anonymized = [];
    selected_word = null;
    window.location = new_url;
}

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
    selected_word = null;
    console.log(words_to_be_anonymized)
    // Document.activeElement.style.opacity = 0;
    window.getSelection().empty();

}

function updateText() {
    base_url = window.location.href.split('?')[0]
    // console.log(base_url)
    new_url = base_url + '?text_param=' + JSON.stringify(words_to_be_anonymized);
    words_to_be_anonymized = [];
    selected_word = null;
    //     setTimeout(function () { window.location = new_url; }, 2000);
    //     // window.location = new_url;
    // }
    window.location = new_url;
}

function updateUserDictionary() {
    base_url = window.location.href.split('?')[0]
    new_url = base_url + '?user_dictionary_param=' + JSON.stringify(words_to_be_anonymized);
    words_to_be_anonymized = [];
    selected_word = null;
    window.location = new_url;
}

function deanonymizeText() {
    base_url = window.location.href.split('?')[0]
    // console.log(base_url)
    new_url = base_url + '?delete_param=' + JSON.stringify(words_to_be_anonymized);
    console.log(words_to_be_anonymized);
    words_to_be_anonymized = [];
    selected_word = null;
    //     setTimeout(function () { window.location = new_url; }, 2000);
    //     // window.location = new_url;
    // }
    window.location = new_url;

}

function deleteWordsToBeAnonymized(n) {
    if (n == -1) {
        words_to_be_anonymized = [];
        base_url = window.location.href.split('?')[0]
        temp = base_url.split('/');
        new_url = '';
        for (i = 0; i < temp.length - 2; i++) {
            new_url += temp[i] + '/';
        }
        id = temp[temp.length - 1];
        new_url += 'delete_anonymized_words/' + id;
        window.location = new_url;

    }
    else if (n > -1) {
        words_to_be_anonymized.splice(n, 1);
    }
    else {
        console.log('Error not valid number of deleteWordsToBeAnonymized array');
    }
};



