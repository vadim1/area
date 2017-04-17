function get_decision_text(decision_type, decision, options, timeframe) {
    var text = 'You are facing a';
    if (decision_type.startsWith('a') || decision_type.startsWith('i')) {
        text += 'n';
    }
    text += ' ' + decision_type + ' challenge.\nYou need to decide ' + decision + '. ';
    text += 'You have these options: ' + options + '.\n';
    var when = '';
    switch (timeframe) {
        case 'day':
            when = 'by the end of the day';
            break;
        case 'week':
            when = 'this week';
            break;
        case 'month':
            when = 'this month';
            break;
        case 'year':
            when = 'this year';
            break;
        case 'sometime':
            when = 'sometime';
            break;
    }
    text += 'You need to decide ' + when + '.';

    return text;
}
