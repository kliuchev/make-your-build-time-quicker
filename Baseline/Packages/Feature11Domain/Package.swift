// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature11Domain",
    products: [.library(name: "Feature11Domain", targets: ["Feature11Domain"])],
    dependencies: [.package(path: "../Shared")],
    targets: [.target(name: "Feature11Domain", dependencies: [.product(name: "Shared", package: "Shared")])]
)
