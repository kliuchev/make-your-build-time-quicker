// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature26Domain",
    products: [.library(name: "Feature26Domain", targets: ["Feature26Domain"])],
    dependencies: [.package(path: "../Shared")],
    targets: [.target(name: "Feature26Domain", dependencies: [.product(name: "Shared", package: "Shared")])]
)
