pub fn sanitize<S: AsRef<str>>(s: S) -> String {
    let input = s.as_ref();
    input.replace("..", "").replace("/", "")
}