# How to do Mapping using Misty Studio

1. Open Misty Studio and navigave to the Explore / Mapping menu.
2. Place Misty with her back to the wall and facing the area you would like her to map.
3. Press the "Start Mapping" button and wait for the little robot icon above the "Start Mapping" button to turn white.
   - This means that Misty has identified her current Pose which means she knows where she is in a 3D space
   - If she loses the pose, a popup will occur to inform you and the icon will turn red. To remedy this, perhaps backtrack Misty to a previous position
4. Move forward around 1 meter and rotate Misty 360 degrees using the controls in the Manual Driving panel. There will be a map starting to form under this panel which updates around every 5 seconds.
5. Repeat step 4 as many times as you think necessary. Check the map visual for updates about what Misty sees.
6. When satisfied, press "Stop Mapping" and wait for the map to finish exporting as indicated by the SLAM Status to the right of the Mapping buttons.
7. If the map doesn't load in, reload the studio and renavigate to the Explore / Mapping menu. Click on the dropdown (which is ordered by data created) and select the most recent map. Press "Display Current Map."
8. If you want the point map, press "Set as Current" and then navigate to Programming / API Explorer. Under Navigation, select "GetMap" and press "Send Request." Copy the output and paste it into a text editor. Format for readability (Prettier in VSCode works well).

# Sources
- https://docs.mistyrobotics.com/misty-ii/misty-studio/mapping/#tips-for-success
- https://docs.mistyrobotics.com/misty-ii/web-api/api-reference/#navigation
