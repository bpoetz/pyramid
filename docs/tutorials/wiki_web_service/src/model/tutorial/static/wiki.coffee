#Simple Coffee script defining functions that consume our wikiwords functions
# usees jQuery



get_page: (event) ->
    wikiword = $(@).html()
    $.ajax({
        url: '127.0.0.1:6543/#{wikiword}',
        }).done(replace_html(data))


edit_page: (event) ->
    wikiword = $(@).html()
    $.ajax({
        type: 'POST',
        url: '127.0.0.1:6543/#{wikiword}/edit_page',
        }).done(replace_html(data))


replace_html: (data) ->
    # for item in data - > flatten page object, then find the css ids on the page and replace the html
    #$(@).html(data[$(@).prop('id')])


$('a.wikiword').on('click', get_page)
$('button#edit').on('click', edit_page)
