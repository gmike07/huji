

export function generateMarker(percents){
    let i = 5 * percents;
    console.log(i);
    let green = Math.min(255, i);
    let red = i <= 255 ? 255: 500 - i;

    return generateMarkerImage(ConvertRGBtoHex(red, green, 0));
}

function ColorToHex(color) {
    var hexadecimal = color.toString(16);
    return hexadecimal.length === 1 ? "0" + hexadecimal : hexadecimal;
}

function ConvertRGBtoHex(red, green, blue) {
    return "#" + ColorToHex(red) + ColorToHex(green) + ColorToHex(blue);
}

function generateMarkerImage(color) {
    const svgMarker = {
        path: "M 12 14 z M 12 2.016 q 2.906 0 4.945 2.039 t 2.039 4.945 q 0 1.453 -0.727 3.328 t -1.758 3.516 t -2.039 3.07 t -1.711 2.273 l -0.75 0.797 q -0.281 -0.328 -0.75 -0.867 t -1.688 -2.156 t -2.133 -3.141 t -1.664 -3.445 t -0.75 -3.375 q 0 -2.906 2.039 -4.945 t 4.945 -2.039 z\n" +
            "M 13.7 9.55 v 4.5 H 10.1 V 9.55 h 3.6 m -0.675 -2.7 h -2.025 l -0.45 0.45 H 8.75 v 0.9 h 6.3 V 7.3 h -1.575 l -0.45 -0.45 z M 14.6 8.65 H 9.2 v 5.4 c 0 0.495 0.405 0.9 0.9 0.9 h 3.6 c 0.495 0 0.9 -0.405 0.9 -0.9 V 8.65 z",
        fillColor: color,
        fillOpacity: 1.0,
        strokeWeight: 0,
        rotation: 0,
        scale: 1.4,
        anchor: new google.maps.Point(15, 30),
    };
    return svgMarker
}

