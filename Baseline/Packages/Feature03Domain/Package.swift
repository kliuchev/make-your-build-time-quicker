// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature03Domain",
    products: [.library(name: "Feature03Domain", targets: ["Feature03Domain"])],
    dependencies: [.package(path: "../Shared")],
    targets: [.target(name: "Feature03Domain", dependencies: [.product(name: "Shared", package: "Shared")])]
)
