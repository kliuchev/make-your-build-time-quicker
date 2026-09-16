// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature09Domain",
    products: [.library(name: "Feature09Domain", targets: ["Feature09Domain"])],
    dependencies: [.package(path: "../Shared")],
    targets: [.target(name: "Feature09Domain", dependencies: [.product(name: "Shared", package: "Shared")])]
)
