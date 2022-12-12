/* Author: Antonio Lang */

// import {MDCTextField} from '@material/textfield';
// import {MDCRipple} from '@material/ripple';

// const MDCTextField = mdc.textField.MDCTextField;
// const textField = new MDCTextField(document.querySelector('.mdc-text-field'));

const MDCButton = mdc.MDCButton;
const buttonRipple = new MDCRipple(document.querySelector('.mdc-button'));
buttonRipple.addEventListener("click", clicked)

function clicked() {
    console.log("Create account button pressed");
}