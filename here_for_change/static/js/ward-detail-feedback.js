
/**
 * Fetches and returns csrf_token stored in html document
 * @returns {String}
 */
function get_csrf_token() {
    return document.querySelector("input[name='csrfmiddlewaretoken']").value;
}


/**
 * Initializes feedback controls [ adds event listeners ]
 */
function init() {
    let feedback_buttons = document.querySelectorAll(".feedback-vote");
    let csrf_token = get_csrf_token();
    feedback_buttons.forEach((button) => {
        button.addEventListener("click", e => {
            if (is_spam(button.dataset.ward, button.dataset.field, button.dataset.action)) {
                return
            };
            data = {
                "action": button.dataset.action,
                "csrfmiddlewaretoken": csrf_token
            };
            updateFeedback(button.dataset.url, data, button.dataset.field);

        });
    });
}


/**
 * Updates feedback counts in back-end server and updates the changes in the User Interface
 * @param {String} url 
 * @param {json} data 
 * @param {String} field 
 */
async function updateFeedback(url, data, field) {
    await postData(url, data).then((responseData) => {
        if (responseData.updated) {
            updateFeedbackValues(field, responseData.feedback);
        }

    });
}


/**
 * Updates feedback values in the User Interface
 * @param {String} field 
 * @param {json} data 
 */
function updateFeedbackValues(field, data) {
    let relatedFeedbackControls = document.querySelectorAll(`.feedback-vote[data-field="${field}"]`);
    for (key of Object.keys(data)) {
        relatedFeedbackControls.forEach((control) => {
            if (control.dataset.action == key) {
                control.querySelector("span:nth-child(3)").innerText = data[key];
            }
        });
    }
}


/**
 * Posts data to backend route
 * @param {String} url 
 * @param {json} data 
 * @returns {json}
 */
async function postData(url, data) {

    const response = await fetch(url, {
        method: 'POST',
        mode: 'cors',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': data.csrfmiddlewaretoken
        },
        body: JSON.stringify(data)
    });
    if (response.status != 200) {
        return { "updated": false };
    }
    return response.json();
}


/**
 * Checks if a click is spam by comparing the current action to action stored in cookie
 * @param {String} ward 
 * @param {String} field 
 * @param {String} action 
 * @returns {Boolean}
 */
function is_spam(ward, field, action) {
    let cookie_value = getCookie(`${ward}-${field}`);
    if (cookie_value !== "") {
        data = parse_to_object(cookie_value);
        if (data.action == action) {
            return true;
        }
    }
    return false;


}


/**
 * Formats and converts json object stored in cookie
 * @param {String} string_object 
 * @returns {json}
 */
function parse_to_object(string_object) {
    string_object = `${string_object}`.replaceAll("\\054", ",");
    string_object = `${string_object}`.replaceAll("\\", "");
    string_object = `${string_object}`.replaceAll(" ", "");
    string_object = `${string_object}`.replaceAll("\"", "\\\"");
    string_object = string_object.substring(1, string_object.length - 2) + "\"";
    return JSON.parse(JSON.parse(string_object));

}


/**
 * Returns value stored with key from cookie
 * @param {String} cname 
 * @returns 
 */
function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}


init();



