// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature27Domain",
    products: [.library(name: "Feature27Domain", targets: ["Feature27Domain"])],
    dependencies: [.package(path: "../Shared")],
    targets: [.target(name: "Feature27Domain", dependencies: [.product(name: "Shared", package: "Shared")])]
)
