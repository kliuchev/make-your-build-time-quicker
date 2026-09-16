// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature01Domain",
    products: [.library(name: "Feature01Domain", targets: ["Feature01Domain"])],
    dependencies: [.package(path: "../Shared")],
    targets: [.target(name: "Feature01Domain", dependencies: [.product(name: "Shared", package: "Shared")])]
)
