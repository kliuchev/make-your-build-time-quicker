import Foundation

func value() -> Data? {
    let encoded: String =
        "S" + "G" + "V" + "s" + "b" + "G8="
    return Data(base64Encoded: encoded, options: [])
}
