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
    it.only("My test written on ubuntu.", () => {
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
})