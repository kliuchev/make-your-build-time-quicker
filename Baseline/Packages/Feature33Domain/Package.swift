// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature33Domain",
    products: [.library(name: "Feature33Domain", targets: ["Feature33Domain"])],
    dependencies: [.package(path: "../Shared")],
    targets: [.target(name: "Feature33Domain", dependencies: [.product(name: "Shared", package: "Shared")])]
)
