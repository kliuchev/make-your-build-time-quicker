// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature02Domain",
    products: [.library(name: "Feature02Domain", targets: ["Feature02Domain"])],
    dependencies: [.package(path: "../Shared")],
    targets: [.target(name: "Feature02Domain", dependencies: [.product(name: "Shared", package: "Shared")])]
)
