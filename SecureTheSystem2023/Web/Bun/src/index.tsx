import { renderToReadableStream } from "react-dom/server"
import { ReactNode } from "react"
import { Card, Row, Col, Container, InputGroup, FormControl, Form, Button } from "react-bootstrap"
import fs from "fs"
import { faker } from "@faker-js/faker"
import { hackerURLParser, isSave } from "./utils/hacker"

type Node = { children: ReactNode }

function MainTemplate({ children }: Node) {
    return (
        <html>
            <head>
                <title>Simple App</title>
                <link rel="stylesheet" href="/assets/css/bootstrap.css" />
            </head>
            <body data-bs-theme="dark">
                <main>
                    <Container>
                        {children}
                    </Container>
                </main>
                <script src="/assets/js/bootstrap.js"></script>
            </body>
        </html>
    )
}

function NotFoundTemplate({ path }: { path: string }) {
    return (
        <MainTemplate>
            <h1>path {path} not found</h1>
        </MainTemplate>
    )
}

function ServerErrorTemplate({ msg }: { msg: string }) {
    return (
        <MainTemplate>
            <h1 className="text-center">505 Something Wrong!</h1>
            <h2 className="text-center">{msg}</h2>
        </MainTemplate>
    )
}

function ChitChatPage({ card }: { card: Array<Array<string>> }) {
    return (
        <MainTemplate>
            <Container className="p-4">
                <h1>Random Hacker Chit Chat Forum</h1>
            </Container>
            <Container>
                <Col className="mb-3">
                    {card.map((val) =>
                        <Row className="p-1">
                            <Card>
                                <Card.Header>
                                    {val[0]}
                                </Card.Header>
                                <Card.Body>
                                    {val[1]}
                                </Card.Body>
                            </Card>
                        </Row>
                    )}
                </Col>
                <Form action="/" method="post">
                    <InputGroup>
                        <InputGroup.Text>Hacker Link</InputGroup.Text>
                        <FormControl
                            placeholder="https://example.com"
                            name="url"
                        />
                        <Button type="submit">send</Button>
                    </InputGroup>
                </Form>
            </Container>
        </MainTemplate>
    )
}

async function fakerResponse() {
    let card = []
    for (let i = 0; i < 3; i++) {
        card.push([faker.person.firstName(), faker.hacker.phrase()])
    }
    return new Response(await renderToReadableStream(<ChitChatPage card={card} />))
}

Bun.serve({
    fetch: async (req, _) => {
        try {
            const url = new URL(req.url)
            if (url.pathname === "/") {
                if (req.method == "GET") {
                    return fakerResponse()
                } else {
                    if (req.body) {
                        const reader = req.body.getReader()
                        const readable = await reader.read()
                        const value = new TextDecoder('utf-8').decode(readable.value)
                        if (typeof value === "string") {
                            if (value.startsWith("url=")) {
                                let urlValue: Function | Object | string
                                if (req.headers.get("Hacker-Token") == Bun.env["Hacker_Token"]) {
                                    urlValue = hackerURLParser(decodeURIComponent(value.substring(4)));
                                } else {
                                    urlValue = decodeURIComponent(value.substring(4))
                                }
                                let data;
                                if (Array.isArray(urlValue)) {
                                    if (await isSave(urlValue)) {
                                        data = Bun.spawnSync({ cmd: ["wget", ...urlValue] })
                                    }
                                } else if (typeof urlValue === "string") {
                                    data = Bun.spawnSync({ cwd: "/tmp/", cmd: ["wget", urlValue, "-O", "-"] })
                                }
                                if (data) {
                                    data = new TextDecoder('utf-8').decode(data.stdout)
                                    data = JSON.parse(data)
                                    return new Response(await renderToReadableStream(<ChitChatPage card={data} />))
                                } else {
                                    return fakerResponse()
                                }
                            }
                        }
                    }
                }
            }
            if (url.pathname.startsWith("/assets")) {
                const pathname = decodeURIComponent(url.pathname)
                if ((/^.*\.(js|css)$/g).test(pathname)) {
                    const assetPath = "./node_modules/bootstrap/dist" + pathname.substring(7, pathname.length)
                    if (fs.existsSync(assetPath)) {
                        const extension = assetPath.split('.').pop()
                        if (extension === 'js') {
                            return new Response(fs.readFileSync(assetPath), {
                                headers: {
                                    "Content-Type": "application/javascript"
                                }
                            })
                        } else if (extension === "css") {
                            return new Response(fs.readFileSync(assetPath), {
                                headers: {
                                    "Content-Type": "text/css"
                                }
                            })
                        } else {
                            return new Response(fs.readFileSync(assetPath))
                        }

                    }
                }
            }
            return new Response(await renderToReadableStream(
                <NotFoundTemplate path={url.pathname} />
            ))
        } catch (error: any) {
            return new Response(await renderToReadableStream(
                <ServerErrorTemplate msg={error.toString()} />
            ))
        }

    },
    port: 8080
})
