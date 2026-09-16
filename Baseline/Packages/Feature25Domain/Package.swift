// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature25Domain",
    products: [.library(name: "Feature25Domain", targets: ["Feature25Domain"])],
    dependencies: [.package(path: "../Shared")],
    targets: [.target(name: "Feature25Domain", dependencies: [.product(name: "Shared", package: "Shared")])]
)
