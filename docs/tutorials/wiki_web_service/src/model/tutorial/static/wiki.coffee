#Simple Coffee script defining functions that consume our wikiwords functions
# usees jQuery
$(->
    get_page = (event) ->

        wikiword = $(@).html()
        $.get(wikiword,).done(replace_html)
        #event.preventDefault()

    edit_page = (event) ->
        #event.preventDefault()
        wikiword = $(@).html()
        $.ajax({
            'type': 'POST',
            'url': wikiword,
            }).done(replace_html)


    replace_html = (data) ->
        # for item in data - > flatten page object, then find the css ids on the page and replace the html
        #$(@).html(data[$(@).prop('id')])


        if data.error?
            $('error').html(data.error)

        if data.page?
            $('name').html(data.page)
            $('data').html(data.data)
            $('updated').html(data.updated)





    $('a.wikiword').on('click', get_page)


    $('button#edit').on('click', edit_page)
)
