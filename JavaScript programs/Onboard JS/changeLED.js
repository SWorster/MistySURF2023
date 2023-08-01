// Julia Yu '24

misty.Debug("Color change time!");

_changeColors();

misty.Debug("color done!");

function _changeColors() {
    misty.ChangeLED(Math.floor(Math.random() * 255), Math.floor(Math.random() * 255), Math.floor(Math.random() * 255));
}