function SensorController() {
    var ctrl = this;

    ctrl.$onInit = function() {
        ctrl.lastSeen = ctrl.formatLastSeen(ctrl.sensor.last_seen);
    };

    ctrl.click = function() {
        ctrl.onClick({ lat: ctrl.sensor.last_lat, lng: ctrl.sensor.last_lng });
    };

    ctrl.formatLastSeen = function(lastSeenDate) {
        var now = new Date();
        
        var lastSeenInMinutes = ctrl.dateDiffInMinutes(new Date(lastSeenDate), now);
        var lastSeenInHours = ctrl.fromMinutesToHours(lastSeenInMinutes);
        var lastSeenInDays = ctrl.fromHoursToDays(lastSeenInHours);
        if (lastSeenInMinutes < 5) {
            return "Less than 5 minutes ago";
        }
        else if (lastSeenInHours === 0) {
            return lastSeenInMinutes + " minutes ago";
        }
        else if (lastSeenInDays === 0) {
            return lastSeenInHours + " hours ago";
        }
        else {
            return lastSeenInDays + " days ago";
        }
    }

    ctrl.dateDiffInMinutes = function(date1, date2) {
        const _MS_PER_MINUTE = 1000 * 60;
        const utc1 = Date.UTC(date1.getFullYear(), date1.getMonth(), date1.getDate());
        const utc2 = Date.UTC(date2.getFullYear(), date2.getMonth(), date2.getDate());
        return Math.floor((utc2 - utc1) / _MS_PER_MINUTE);
    }

    ctrl.fromMinutesToHours = function(minutes) {
        const _MINUTES_PER_HOUR = 60;
        return Math.floor(minutes / _MINUTES_PER_HOUR);
    }

    ctrl.fromHoursToDays = function(hours) {
        const _HOURS_PER_DAY = 24;
        return Math.floor(hours / _HOURS_PER_DAY);
    }
}

app.component('rmSensor', {
    templateUrl: 'rm-sensor.html',
    controller: SensorController,
    bindings: {
        sensor: '<',
        onClick: '&'
    }
});