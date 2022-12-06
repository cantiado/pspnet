import {MDCTextField} from '@material/textfield';
import {MDCRipple} from '@material/ripple';

const textField = new MDCTextField(document.querySelector('.mdc-text-field'));

const buttonRipple = new MDCRipple(document.querySelector('.mdc-button'));
buttonRipple.addEventListener("click", ()=>console.log("Clicked"))