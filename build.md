[app] {

}

[bot] {
actions: [
"Gathering",
"Solving Puzzle",
"Combat/Escaping",
"Kill monsters around it",
"Check Inventory"
]
mouse-movements: "user-like",

}

now we need to upgrade the dashboard and UI:

- build the ability of add/remove/modify for active game windows with [window title, notify me checker] (saved inside user-pref).
- New settings (saved inside user-pref):
- - can modify the item priority.
- - can modify the item notification sound (from list provided, will be triggered based on top item priority detected in that moment).
- - check if want auto save for changes.
- - checker for (root.attributes("-topmost", True)) while the app running.
- - custom themes listed.
- - open/close for (CPU healthcare).
- - open/close for OS notification (if the user away from any of that app or game windows).
- when detecting the items, it can appears detected at most 5 items in that moment (instead of detected \* item).
- remove ("F9" and loot_active_target) level (no need for that layer, i should to active myself when go to the game window to loot).
- CPU health checker.
- for each window add its status in the top-right.
- better UI design and layout.
