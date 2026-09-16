// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature08Domain",
    products: [.library(name: "Feature08Domain", targets: ["Feature08Domain"])],
    dependencies: [.package(path: "../Shared")],
    targets: [.target(name: "Feature08Domain", dependencies: [.product(name: "Shared", package: "Shared")])]
)
