describe('My test suite', () => {
    it('My first test case', () => {
        cy.request({
            method: 'GET',
            url: 'http://127.0.0.1:8000/'
        }).then(response => {
            const data = response.body
            expect(data).to.be.an('object')
            expect(data).to.have.property('Hello')
            expect(data.Hello).to.be.an('string')
            expect(data.Hello).to.be.eq('World')
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
            expect(response.status).to.be.eq(422)
            expect(response.body.detail[0].msg).to.be.eq("Input should be a valid integer, unable to parse string as an integer")
            expect(response.body.detail[0].type).to.be.eq("int_parsing")
        })
    })
    it("Test for requesting the post contact route.", () => {
        cy.request({
            method: 'POST',
            url: 'http:/127.0.0.1:8000/contacts',
            failOnStatusCode: false,
            body: {
                id: 5,
                name: 'Iden',
                last_name: 'Ticlla',
                age: 25,
                phone_number: 77478489
            }
        }).then(response => {
            expect(response.status).to.be.eq(201)
            const data = response.body
            expect(data).to.be.an('object')
            expect(data.name).to.be.eq('Iden')
            expect(data.last_name).to.be.eq('Ticlla') 
            expect(data.age).to.be.eq(25) 
            expect(data.phone_number).to.be.eq(77478489) 
        })
    })
    it("Testing the login functionality - expecting 400 status.", () => {
        cy.request({
            method: 'POST',
            url : 'http://127.0.0.1:8000/login',
            failOnStatusCode: false,
            // form: true,
            headers: {
                // 'Content-Type': 'application/x-www-form-urlencode'
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            },
            body: {
                username: 'asdf',
                password: 'somepassword'
            }
        }).then(response => {
            expect(response.status).to.be.eq(400)
            const msg = response.body.detail
            expect(msg).to.be.eq("Wrong username or password.")
        })
    })
    it("Testing the login functionality expecting 200 status", () => {
        cy.request({
            method: 'POST',
            url: 'http://127.0.0.1:8000/login',
            failOnStatusCode: false,
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            },
            body: {
                username: 'jhondoe',
                password: 'secret1'
            }
        }).then(response => {
            expect(response.status).to.be.eq(200)
            const data = response.body
            expect(data).to.have.property("access_token")
            expect(data).to.have.property("token_type")
            expect(data.token_type).to.be.eq('bearer')
        })
    })
    it("Testing the get me endpoint with inactive user.", () => {
        cy.request({
            method: 'POST',
            url: 'http://127.0.0.1:8000/login',
            failOnStatusCode: false,
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            },
            body: {
                username: 'alice',
                password: 'secret1'
            }
        }).then(response => {
            const token = response.body.access_token
            cy.request({
                method: 'GET',
                url: 'http://127.0.0.1:8000/users/me',
                failOnStatusCode: false,
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            }).then(response => {
                expect(response.status).to.be.eq(400)
                expect(response.body.detail).to.be.eq('Inactive user')
            })
        })
    })
    it("Test for testing the get me endpoint with active user.", () => {
        cy.request({
            method: "POST",
            url: "http://127.0.0.1:8000/login",
            failOnStatusCode: false,
            headers: {
                "Content-Type": 'application/x-www-form-urlencoded; charset=UTF-8'
            },
            body: {
                username: "jhondoe",
                password: "secret1"
            }
        }).then(response => {
            const token = response.body.access_token
            cy.request({
                method: 'GET',
                url: 'http://127.0.0.1:8000/users/me',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            }).then(response => {
                expect(response.status).to.be.eq(200)
                expect(response.body).to.be.an('object')
                expect(response.body.username).to.be.eq('jhondoe')
                expect(response.body.phone).to.be.eq("77074485")
                expect(response.body.email).to.be.eq('jhondoe@gmail.com')
                expect(response.body.age).to.be.eq(19)
                expect(response.body.disabled).to.be.eq(false)
            })
        })
    })
    it ("Test for testing query parameters without providing them", () => {
        cy.request({
            method: 'GET',
            url: 'http://127.0.0.1:8000/contacts'
        }).then(response => {
            const data = response.body
            expect(data).to.have.length(5)
        })
    })
    it('Test for testing query parameters providing them - 1', () => {
        cy.request({
            method: 'GET',
            url: 'http://127.0.0.1:8000/contacts?skip=1&limit=10'
        }).then(response => {
            const data = response.body
            expect(data).to.have.length(4)
        })
    })

    it('Test for testing query parameters providing them - 2', () => {
        cy.request({
            method: 'GET',
            url: 'http://127.0.0.1:8000/contacts?skip=2&limit=10'
        }).then(response => {
            const data = response.body
            expect(data).to.have.length(3)
        })
    })

    it('Test for testing query parameters providing them - 3', () => {
        cy.request({
            method: 'GET',
            url: 'http://127.0.0.1:8000/contacts?skip=10&limit=10'
        }).then(response => {
            const data = response.body
            expect(data).to.have.length(0)
        })
    })
    it("Test for testing required query parameters. - 1", () => {
        cy.request({
            method: 'GET',
            url: 'http://127.0.0.1:8000/query_parameters/required',
            failOnStatusCode: false
        }).then(response => {
            console.log(response)
            console.log(response.body)
            const data = response.body.detail
            const param1 = data[0]
            const param2 = data[1]
            const msgForParam1 = param1.msg
            expect(msgForParam1).to.be.eq('Field required')
            const msgForParam2 = param2.msg
            expect(msgForParam2).to.be.eq('Field required')

        })
    })
    it("Test for testing not required query parameters", () => {
        cy.request({
            method: "GET",
            url: 'http://127.0.0.1:8000/query_parameters/notrequired',
        }).then(response => {
            const parameter1 = response.body.parameter1
            const parameter2 = response.body.parameter2
            expect(parameter1).to.be.eq(null)
            expect(parameter2).to.be.eq(null)
        })
    })
    it("Test for testing the path parameter endpoint with valid param data type.", () => {
        cy.request({
            method: 'GET',
            failOnStatusCode: false,
            url: 'http://127.0.0.1:8000/path_parameter/1'
        }).then(response => {
            const data = response.body
            expect(data.path_parameter).to.be.eq(1)
        })
    })
    it("Test for testing the path parameter endpoint with invalid param data type.", () => {
        cy.request({
            method: 'GET',
            failOnStatusCode: false,
            url: 'http://127.0.0.1:8000/path_parameter/helloworld'
        }).then(response => {
            const data = response.body.detail
            expect(data[0].type).to.be.eq("int_parsing")
            expect(data[0].msg).to.be.eq("Input should be a valid integer, unable to parse string as an integer")
            expect(data[0].input).to.be.eq("helloworld")
            expect(data[0].loc[0]).to.be.eq('path')
            expect(data[0].loc[1]).to.be.eq('item_id')
        })
    })
    it("Test for testing the bool query parameter - 1.", () => {
        cy.request({
            method: 'GET',
            url: 'http://127.0.0.1:8000/query_parameters/booleans/?boolean=yes'
        }).then(response => {
            const data = response.body
            expect(data.boolean).to.be.eq(true)
        })
    })

    it("Test for testing the bool query parameter - 2.", () => {
        cy.request({
            method: 'GET',
            url: 'http://127.0.0.1:8000/query_parameters/booleans/?boolean=no'
        }).then(response => {
            const data = response.body
            expect(data.boolean).to.be.eq(false)
        })
    })
    it("Test for testing the path query body parameters.", () => {
        cy.request({
            method: 'GET',
            url: 'http://127.0.0.1:8000/path_query_body_parameters/qwerty?query=zxcv',
            body: {
                username: 'asdf',
                phone: '74879998',
                email: 'asdf@gmail.com',
                age: 20,
                disabled: false
            }
        }).then(response => {
            console.log(response)
            const data = response.body
            console.log(data)
            expect(data.path).to.be.eq('qwerty')
            expect(data.query).to.be.eq('zxcv')
            expect(data.user).to.be.an('object')
        })
    })

    it.only("Test for testing the string validations.", () => {
        cy.request({
            method: 'GET',
            failOnStatusCode: false,
            url: 'http://127.0.0.1:8000/validations/string?q=asdfzxcvzncvvnqwerweqqwerwqewwrqwerqwerwqerasdfzxcvzncvvnqwerweqqwerwqewwrqwerqwerwqer'
        }).then(response => {
            expect(response.body.detail[0].type).to.be.eq("string_too_long")
            expect(response.body.detail[0].msg).to.be.eq("String should have at most 50 characters")
        })
    })

    it.only("Test for testing the integer validations.", () => {
        cy.request({
            method: 'GET',
            failOnStatusCode: false,
            url: 'http://127.0.0.1:8000/validations/integer?q=0'
        }).then(response => {
            console.log(response)
            expect(response.body.detail[0].type).to.be.eq("greater_than")
            expect(response.body.detail[0].msg).to.be.eq("Input should be greater than 0")
        })
    })
})
