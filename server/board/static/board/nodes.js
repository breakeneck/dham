$(function () {
    $('.action').click(function () {
        [node_id, action_id] = [$(this).data('node_id'), $(this).data('action_id')];
        $.getJSON('/run/' + node_id + '/' + action_id, {},
            (response) => $(this).closest('.card').find('.response').text(JSON.stringify(response, null, 2)));
        return false;
    });
});