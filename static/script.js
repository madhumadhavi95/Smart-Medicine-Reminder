// Request notification permission
if ("Notification" in window) {
    Notification.requestPermission();
}
console.log(Notification.permission);


const reminderSound = new Audio("/static/reminder.mp3");

setInterval(function () {

    let now = new Date();

    let currentDate = now.toISOString().split("T")[0];

    let currentTime =
        now.getHours().toString().padStart(2, "0") + ":" +
        now.getMinutes().toString().padStart(2, "0");

    let rows = document.querySelectorAll("table tr");

    rows.forEach((row, index) => {

        if (index === 0) return;

        let medicine = row.cells[1].innerText;
        let date = row.cells[2].innerText;
        let time = row.cells[3].innerText;

        if (date === currentDate && time === currentTime) {

            reminderSound.play();

            if (Notification.permission === "granted") {
                new Notification("💊 Medicine Reminder", {
                    body: "⏰ Time to take: " + medicine
                });
            }

            alert("⏰ Time to take: " + medicine);
        }

    });

}, 60000);