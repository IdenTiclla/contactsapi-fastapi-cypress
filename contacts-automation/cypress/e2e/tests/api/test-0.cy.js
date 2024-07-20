describe('My test suite', () => {
    it('My first test case', () => {
        cy.request({
            method: 'GET',
            url: 'http://127.0.0.1:8000/'
        }).then(response => {
            console.log(response)
            console.log(response.body)
            const data = response.body
            expect(data).to.be.an('object')
            expect(data).to.have.property('Hello')
            expect(data.Hello).to.be.an('string')
            expect(data.Hello).to.be.eq('World')
        })
    })
    it("My second test case.", () => {
        cy.request({
            method: 'GET',
            url: 'http://127.0.0.1:8000/name'
        }).then(response => {
            const data = response.body
            expect(data).to.be.an('object')
            expect(data).to.have.property('name')
            expect(data.name).to.be.eq('Iden')
            expect(data.name).to.be.an('string')
        })
    })
    it("My test written on ubuntu.", () => {
        cy.request({
            method: 'GET',
            url: 'http://127.0.0.1:8000/ubuntu'
        }).then(response => {
            expect(response.status).to.be.eq(200)
            const data = response.body
            expect(data).to.be.an('object')
            expect(data).to.have.property('os')
            expect(data.os).to.be.an('string')
            expect(data.os).to.be.eq('ubuntu')
        })
    })

    it("My test written on windows", () => {
        cy.request({
            method: 'GET',
            url: 'http://127.0.0.1:8000/windows'
        }).then(response => {
            const data = response.body
            expect(data).to.be.an('object')
            expect(data).to.have.property('os')
            expect(data.os).to.be.an('string')
            expect(data.os).to.be.eq('windows')
        })
    })
    it("Test for the users route.", () => {
    	cy.request({
	        method: 'GET',
	        url: 'http:/127.0.0.1:8000/users'
	    }).then(response => {
            const data = response.body
            expect(data.users).to.be.an('array')
            expect(data.users[0].name).to.be.eq('juan')
            expect(data.users[1].name).to.be.eq('brayan')
	    })
    })
    it("Test for the update users route.", () => {
        cy.request({
            method: 'PUT',
            url: 'http:/127.0.0.1:8000/users/1'
        }).then(response => {
            console.log(response)
            expect(response.body.msg).to.be.eq('user with the id: 1 was updated successfully')
        })
    })

    it("Test for requesting the update users route but with not valid parameters.", () => {
        cy.request({
            method: 'PUT',
            url: 'http:/127.0.0.1:8000/users/asdf',
            failOnStatusCode: false
        }).then(response => {
            const data = response.body
            expect(response.status).to.be.eq(422)
            expect(data.detail[0].msg).to.be.eq('Input should be a valid integer, unable to parse string as an integer')
        })
    })
    it("Test for requesting the delete users route.", () => {
        cy.request({
            method: 'DELETE',
            url: 'http:/127.0.0.1:8000/users/1'
        }).then(response => {
            console.log(response)
            expect(response.status).to.be.eq(200)
            expect(response.body.msg).to.be.eq('user with the id: 1 was deleted successfully')
        })
    })
    it("Bad request for the delete users route.", () => {
        cy.request({
            method: 'DELETE',
            url: 'http:/127.0.0.1:8000/users/asdfd',
            failOnStatusCode: false
        }).then(response => {
            console.log(response)
            expect(response.status).to.be.eq(422)
            expect(response.body.detail[0].msg).to.be.eq("Input should be a valid integer, unable to parse string as an integer")
            expect(response.body.detail[0].type).to.be.eq("int_parsing")
        })
    })
    it("Test for requesting the post contact route.", () => {
        cy.request({
            method: 'POST',
            url: 'http:/127.0.0.1:8000/contacts',
            body: {
                name: 'Iden',
                last_name: 'Ticlla',
                age: 25,
                phone_number: 77478489
            }
        }).then(response => {
            console.log(response)
            expect(response.status).to.be.eq(200)
            const data = response.body
            expect(data.msg).to.be.eq("user created successfully.")
            expect(data.contact.name).to.be.eq('Iden')
            expect(data.contact.last_name).to.be.eq('Ticlla') 
            expect(data.contact.age).to.be.eq(25) 
            expect(data.contact.phone_number).to.be.eq(77478489) 
        })
    })
    it.only("Testing the login functionality.", () => {
        cy.request({
            method: 'POST',
            url : 'http:/127.0.0.1:8000/login',
            failOnStatusCode: false,
            form: true,
            body: {
                username: 'asdf',
                password: 'somepassword'
            }
        }).then(response => {
            expect(response.status).to.be.eq(400)
            const msg = response.body.detail
            expect(msg).to.be.eq("Incorrect username or password.")
        })
    })
})
