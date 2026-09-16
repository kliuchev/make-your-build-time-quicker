// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature28Domain",
    products: [.library(name: "Feature28Domain", targets: ["Feature28Domain"])],
    dependencies: [.package(path: "../Shared")],
    targets: [.target(name: "Feature28Domain", dependencies: [.product(name: "Shared", package: "Shared")])]
)
