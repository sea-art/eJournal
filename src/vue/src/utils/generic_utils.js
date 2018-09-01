/* Expects a start date of the format "YY-mm-dd" */
export default {
    yearOffset (startDate) {
        let split = startDate.split('-')
        let yearOff = parseInt(split[0]) + 1

        split[0] = String(yearOff)
        return split.join('-')
    }
}
