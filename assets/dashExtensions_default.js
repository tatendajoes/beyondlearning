window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(params) {
            const std = ['copy', 'paste'];
            const canDelete = !params.node.data.has_session;
            const del = {
                name: 'Delete row',
                disabled: !canDelete,
                action: () => {
                    // Push class_id into a hidden div so Dash picks it up
                    document.getElementById('delete-sentinel')
                        .setAttribute('data-cid', params.node.data.class_id);
                }
            };
            return std.concat(['separator', del]);
        }

    }
});