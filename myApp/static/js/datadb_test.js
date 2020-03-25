var datatable = new DataTable(document.querySelector('#first-datatable-output table'), {
    pageSize: 5,
    sort: [true, true, false],
    filters: [true, false, 'select'],
    filterText: 'Type to filter... ',
    pagingDivSelector: "#paging-first-datatable"
});
